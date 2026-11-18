#!/usr/bin/env python3
"""Read-only, stdlib-only font-size gate using native PPTX points (not width-scaled).

Does not inspect rasterized words inside images, line wrapping, font substitution,
RTL UI state or semantic correctness: those require separate visual/PowerPoint QA.
"""
import argparse
import json
import posixpath
import re
import sys
import zipfile
from collections import Counter
from xml.etree import ElementTree as ET

EMU_PER_INCH = 914400
NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS_RELS = 'http://schemas.openxmlformats.org/package/2006/relationships'
NS = {'p': NS_P, 'a': NS_A, 'r': NS_R}
T = lambda uri, name: f'{{{uri}}}{name}'


def get_slide_paths(z, pres):
    """Presentation-order slide paths, not filename-alphabetical order."""
    relationship_path = 'ppt/_rels/presentation.xml.rels'
    try:
        rels = ET.fromstring(z.read(relationship_path))
        ids = {rel.get('Id'): rel.get('Target') for rel in rels.findall(T(NS_RELS, 'Relationship'))}
        order = []
        for elem in pres.findall('.//p:sldIdLst/p:sldId', NS):
            relid = elem.get(T(NS_R, 'id'))
            target = ids.get(relid)
            if not target:
                raise ValueError(f'Cannot resolve relationship: {relid}')
            if target.startswith('/'):
                path = target.lstrip('/')
            else:
                path = posixpath.normpath(posixpath.join('ppt', target))
            if path not in z.namelist():
                raise ValueError(f'Slide not found in archive: {path}')
            order.append(path)
        return order
    except KeyError as err:
        raise ValueError(f'Missing presentation relations: {err}')


def font_pt(node, fallback):
    val = node.get('sz') if node is not None else None
    if val is None:
        return fallback
    try:
        return int(val) / 100.0  # DrawingML font sizes use hundredths of a point
    except (ValueError, TypeError):
        return None


def text_body_runs(body, width_in, minimum, ref_width, table_position=None):
    """Read direct paragraphs in either a shape or a native table cell.

    The cell owns its own list-style defaults; a shape-level search would miss
    those defaults or accidentally inherit the style of a different cell.
    """
    text_parts, size_records = [], []
    for paragraph_index, para in enumerate(body.findall('a:p', NS), start=1):
        ppr = para.find('a:pPr', NS)
        default_rpr = ppr.find('a:defRPr', NS) if ppr is not None else None
        fallback = font_pt(default_rpr, None)
        if fallback is None:
            level = int(ppr.get('lvl', '0')) if ppr is not None else 0
            level_pr = body.find(f'a:lstStyle/a:lvl{level+1}pPr/a:defRPr', NS)
            fallback = font_pt(level_pr, None)
        chunks = []
        text_run_index = 0
        for child in para:
            if child.tag not in (T(NS_A, 'r'), T(NS_A, 'fld')):
                continue
            txt = child.find('a:t', NS)
            if txt is None or not txt.text or not txt.text.strip():
                continue
            text_run_index += 1
            chunks.append(txt.text)
            record = {'text': txt.text, 'paragraph_index': paragraph_index,
                      'run_index': text_run_index}
            if table_position is not None:
                record.update({'table_row': table_position[0],
                               'table_column': table_position[1]})
            sz = font_pt(child.find('a:rPr', NS), fallback)
            if sz is None:
                record['status'] = 'unresolved'
            else:
                eff = sz * ref_width / width_in
                record.update({'native_pt': round(sz, 3),
                               'reference_equivalent_pt_info_only': round(eff, 3),
                               'status': 'FAIL' if sz + 1e-8 < minimum else 'PASS'})
            size_records.append(record)
        if chunks:
            text_parts.append(''.join(chunks))
    return text_parts, size_records


def element_report(slide, shape_id, shape_name, container_type, text_parts,
                   size_records, unverified_reason=None):
    if not size_records and not unverified_reason:
        return None
    statuses = {item['status'] for item in size_records}
    status = ('FAIL' if 'FAIL' in statuses else
              ('UNVERIFIED' if 'unresolved' in statuses or unverified_reason else 'PASS'))
    result = {'slide': slide, 'shape_id': shape_id, 'shape_name': shape_name,
              'container_type': container_type,
              'text_excerpt': ' | '.join(text_parts)[:140], 'status': status,
              'runs': size_records}
    if unverified_reason:
        result['unverified_reason'] = unverified_reason
    return result


def parse_slide(z, path, number, width_in, minimum, ref_width):
    doc = ET.fromstring(z.read(path))
    shape_reports = []
    for shape_type, container_type in [('sp', 'shape'), ('cxnSp', 'connector')]:
        for shape in doc.findall(f'.//p:{shape_type}', NS):
            body = shape.find('p:txBody', NS)
            if body is None:
                continue
            props = 'p:nvSpPr/p:cNvPr' if shape_type == 'sp' else 'p:nvCxnSpPr/p:cNvPr'
            c = shape.find(props, NS)
            shape_id = c.get('id') if c is not None else None
            shape_name = c.get('name') if c is not None else None
            parts, runs = text_body_runs(body, width_in, minimum, ref_width)
            report = element_report(number, shape_id, shape_name, container_type,
                                    parts, runs)
            if report is not None:
                shape_reports.append(report)

    for frame in doc.findall('.//p:graphicFrame', NS):
        c = frame.find('p:nvGraphicFramePr/p:cNvPr', NS)
        shape_id = c.get('id') if c is not None else None
        shape_name = c.get('name') if c is not None else None
        graphic_data = frame.find('a:graphic/a:graphicData', NS)
        table = graphic_data.find('a:tbl', NS) if graphic_data is not None else None
        if table is None:
            # Native charts, SmartArt and other graphic frames may have editable
            # text in related parts. Do not silently turn skipped text into PASS.
            kind = 'native_chart_or_other_graphic_frame'
            reason = 'Editable text in this native graphic frame is not measured'
            shape_reports.append(element_report(number, shape_id, shape_name,
                                                kind, [], [], reason))
            continue
        text_parts, size_records = [], []
        for row_index, row in enumerate(table.findall('a:tr', NS), start=1):
            for cell_index, cell in enumerate(row.findall('a:tc', NS), start=1):
                body = cell.find('a:txBody', NS)
                if body is None:
                    continue
                parts, runs = text_body_runs(body, width_in, minimum, ref_width,
                                             (row_index, cell_index))
                text_parts.extend(parts)
                size_records.extend(runs)
        report = element_report(number, shape_id, shape_name, 'native_table',
                                text_parts, size_records)
        if report is not None:
            shape_reports.append(report)

    total_native = len(shape_reports)
    total_runs = sum(len(item['runs']) for item in shape_reports)
    fail = sum(item['status'] == 'FAIL' for item in shape_reports)
    unresolved = sum(item['status'] == 'UNVERIFIED' for item in shape_reports)
    return {'slide': number, 'text_shapes': total_native, 'text_runs': total_runs,
            'failed_shapes': fail, 'unverified_shapes': unresolved,
            'failures': [x for x in shape_reports if x['status'] == 'FAIL'],
            'unverified': [x for x in shape_reports if x['status'] == 'UNVERIFIED'],
            'all_text_elements': shape_reports}


def scan(path, minimum, ref_width):
    with zipfile.ZipFile(path) as z:
        pres = ET.fromstring(z.read('ppt/presentation.xml'))
        size = pres.find('p:sldSz', NS)
        if size is None:
            raise ValueError('Missing slide size')
        width = int(size.get('cx')) / EMU_PER_INCH
        height = int(size.get('cy')) / EMU_PER_INCH
        if width <= 0:
            raise ValueError('Invalid slide width')
        paths = get_slide_paths(z, pres)
        slides = [parse_slide(z, p, i + 1, width, minimum, ref_width) for i, p in enumerate(paths)]
    total_fail = sum(s['failed_shapes'] for s in slides)
    total_unverified = sum(s['unverified_shapes'] for s in slides)
    status = 'REVISE' if total_fail else ('UNVERIFIED' if total_unverified else 'PASS_FONT_METADATA')
    return {
        'file': path, 'slide_count': len(slides),
        'slide_dimensions_in': {'width': round(width, 4), 'height': round(height, 4)},
        'gate_basis': 'native_pt', 'minimum_native_pt': minimum,
        'reference_slide_width_in_info_only': ref_width, 'legacy_equivalent_native_threshold_info_only': round(minimum * width / ref_width, 3),
        'native_text_shapes': sum(x['text_shapes'] for x in slides),
        'failed_shapes': total_fail, 'unverified_shapes': total_unverified,
        'failed_slide_numbers': [x['slide'] for x in slides if x['failed_shapes']],
        'result': status, 'slides': slides,
        'limitations': [
            'Measures editable native shape and table-cell text; other graphic frames (including charts) are explicitly UNVERIFIED.',
            'A chart or other unsupported native graphic frame requires additional font verification before overall PASS.',
            'Includes successful, failed and unresolved native runs in slides[].all_text_elements.',
            'Text baked into images is outside native font-size metadata and requires visual review.',
            'Missing font-size inheritance is UNVERIFIED, never treated as PASS.',
            'No scaling for gate: directly compare each native_pt with minimum_native_pt, regardless of slide width.',
            'Reference equivalent sizes are for information only and must not alter PASS/REVISE.',
            'Font-size metadata does not prove visual legibility, correct RTL, or absence of clipping.',
            'Native font availability and semantic visual validation require separate review.'
        ]
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pptx', help='PowerPoint exported from Canva')
    parser.add_argument('--minimum', type=float, default=18.0)
    parser.add_argument('--reference-width', type=float, default=40.0 / 3.0,
                        help='For informational comparison only; does not affect the native-pt gate')
    parser.add_argument('--output', help='JSON report path (otherwise stdout)')
    args = parser.parse_args()
    try:
        report = scan(args.pptx, args.minimum, args.reference_width)
    except Exception as exc:
        print(json.dumps({'result': 'BLOCKER', 'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    data = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(data + '\n')
    else:
        print(data)
    print(f"Font gate: {report['result']}; {report['failed_shapes']} failed of {report['native_text_shapes']} native text shapes, {report['unverified_shapes']} unverified; failed slides {report['failed_slide_numbers']}", file=sys.stderr)
    return 0 if report['result'] == 'PASS_FONT_METADATA' else 1


if __name__ == '__main__':
    raise SystemExit(main())
