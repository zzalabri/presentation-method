# منهج إنشاء العروض التقديمية — Presentation Method

> **حزمة التشغيل المعتمدة V1.2.1** — للاستخدام من حسابات ChatGPT المختلفة دون الحاجة إلى تفعيل إضافة GitHub أو Google Drive لقراءة قواعد المنهج.
>
> هذا المستودع يضم **ملفات التشغيل الأصلية السبعة**، بالإضافة إلى **أجزاء قراءة اختيارية** تسهّل فتح النصوص الطويلة دون إضافات. ملفات الأرشيف والتجارب وسجلات التطوير السابقة غير مشمولة، كما أن أوراق البحث والعروض المنتجة ليست جزءًا منه.

## ابدأ من هنا

**[افتح مدخل التشغيل 40 — نص مباشر (RAW)](https://raw.githubusercontent.com/zzalabri/presentation-method/main/40_OPERATING_ENTRYPOINT.md)**

اقرأ المدخل، ثم راجع الملفات التشغيلية التي يُحيل إليها حسب نوع المهمة. لعرض جديد، تحقق من قراءة المراجع 35 و36 و37 قبل مراحلها المعنية، واستخدم 41 قالبًا لسجل حالة المهمة الجديدة. **إذا تعذر جلب نص مرجع طويل كاملًا، استخدم [فهرس القراءة المجزأة](https://raw.githubusercontent.com/zzalabri/presentation-method/main/reading/INDEX.md) قبل طلب أي ملفات من المستخدم.**

| الملف | دوره | رابط النص المباشر |
|---|---|---|
| `40_OPERATING_ENTRYPOINT.md` | المدخل الرئيسي وتحديد النمط وبوابة جاهزية الوصول | [RAW](https://raw.githubusercontent.com/zzalabri/presentation-method/main/40_OPERATING_ENTRYPOINT.md) |
| `35_V1.2.1_OPERATING_SOURCE_REVIEW.md` | قواعد الإنتاج والتنفيذ | [RAW](https://raw.githubusercontent.com/zzalabri/presentation-method/main/35_V1.2.1_OPERATING_SOURCE_REVIEW.md) |
| `36_V1.2.1_ACCEPTANCE_SOURCE_REVIEW.md` | بوابات القبول وضمان الجودة | [RAW](https://raw.githubusercontent.com/zzalabri/presentation-method/main/36_V1.2.1_ACCEPTANCE_SOURCE_REVIEW.md) |
| `37_SOURCE_EXTRACTION_MULTI_PASS_REVIEW.md` | مراجعة استخراج مادة البحث | [RAW](https://raw.githubusercontent.com/zzalabri/presentation-method/main/37_SOURCE_EXTRACTION_MULTI_PASS_REVIEW.md) |
| `41_DECK_STATE_TEMPLATE.md` | قالب سجل حالة مستقل لكل عرض | [RAW](https://raw.githubusercontent.com/zzalabri/presentation-method/main/41_DECK_STATE_TEMPLATE.md) |
| `32_PPTX_FONT_GATE_NATIVE_PT.py` | أداة اختيارية لفحص قياسات الخطوط داخل PPTX بعد التصدير | [RAW](https://raw.githubusercontent.com/zzalabri/presentation-method/main/32_PPTX_FONT_GATE_NATIVE_PT.py) |
| `AGENTS.md` | تعليمات بدء التشغيل في بيئات الوكلاء | [RAW](https://raw.githubusercontent.com/zzalabri/presentation-method/main/AGENTS.md) |

## شروط أساسية

- **لا حاجة إلى Plugin لقراءة الملفات العامة** إذا كانت قدرة فتح روابط الويب المباشرة متاحة؛ تحقق من النص الفعلي لكل مرجع قبل المتابعة. إذا اختصر التصفح نصًا طويلًا، انتقل أولًا إلى [أجزاء القراءة](https://raw.githubusercontent.com/zzalabri/presentation-method/main/reading/INDEX.md) بالترتيب. اطلب إرفاق المرجع المحدد فقط إن لم تنجح روابطه المباشرة وأجزاؤه، ولا تفترض قراءته.
- **العمل مستقل:** كل عرض جديد يبدأ من ملف البحث الذي يحدده المستخدم، دون البحث في عروض Canva السابقة أو ملفات مشاريع مشابهة، ولا يستعيد عرضًا سابقًا من تلقاء نفسه.
- **التصميم إبداعي افتراضيًا:** طبّق `CREATIVE-BY-DEFAULT` و`VISUAL-DIRECTION-FIRST` و`CREATIVE-SAMPLE-LOCK`، مع عرض **ثلاث شرائح Canva فعلية** للاعتماد قبل استكمال العرض وفق البوابات المعتمدة.
- **ملف البحث منفصل:** يُرفق ملف DOCX/PDF الخاص بكل مهمة أو يُتاح الوصول الصريح إليه؛ وجود رابط أو مسار Google Drive خاص لا يعني أن الحساب الآخر يستطيع قراءته.
- **الأدوات مستقلة عن المنهج:** توفر ملفات المنهج لا يثبت توفر Canva أو صلاحياته. طبّق `ACCESS-PREFLIGHT-GATE` وسجّل `ACCESS_BLOCKER` إذا تعذر تنفيذ تكليف كامل.
- **التصدير:** يظل تصدير PPTX من Canva بيد المستخدم افتراضيًا (`USER-EXPORT-ONLY`)، ثم تُفحص النسخة المرفوعة وفق المنهج؛ لا تدّع تسليم ملف لم يُصدر.

## مطالبة بدء قصيرة لأي حساب ChatGPT

> استخدم «منهج إنشاء العروض التقديمية» من [مدخل التشغيل المباشر](https://raw.githubusercontent.com/zzalabri/presentation-method/main/40_OPERATING_ENTRYPOINT.md). اقرأ **النص الكامل** للمدخل ومراجعه 35 و36 و37 حسب الإحالات؛ إذا قُطع ملف طويل فاستخدم [فهرس القراءة على أجزاء](https://raw.githubusercontent.com/zzalabri/presentation-method/main/reading/INDEX.md) حتى يكتمل قبل البدء. استخدم ملف البحث الذي أرفقه أو أحدده فقط، وأنشئ عرضًا جديدًا مستقلًا بإبداع بصري مرتفع، مع بوابة اعتماد ثلاث شرائح Canva فعلية، وبقية بوابات المنهج. لا تبحث عن عروض قديمة ولا تستبدل التنفيذ بخطة نظرية. إذا تعذرت قراءة مرجع أو ملف المصدر أو إتاحة Canva، حدد العائق الفعلي واطلب الحل الأدنى مرة واحدة دون تخمين التنفيذ.

هذه النسخة من الملفات للنشر على GitHub فقط؛ لم تُعدّل النسخ الأصلية في Google Drive. مراجع تطوير المنهج التاريخية، مثل 38 و42، موجودة خارج حزمة التشغيل وليست متطلبات لإنتاج عرض جديد.
