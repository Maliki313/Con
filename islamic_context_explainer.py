"""
شارح السياق الثقافي الإسلامي التفاعلي
نظام متقدم لشرح المفاهيم الإسلامية مع السياق الثقافي والتاريخي
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class ConceptCategory(Enum):
    """تصنيفات المفاهيم الإسلامية"""
    WORSHIP = "عبادات"
    BELIEFS = "عقائد"
    JURISPRUDENCE = "فقه"
    HISTORY = "تاريخ"
    ETHICS = "أخلاق"
    CULTURE = "ثقافة"
    SPIRITUALITY = "روحانيات"
    TERMINOLOGY = "مصطلحات"

@dataclass
class IslamicConcept:
    """هيكل بيانات المفاهيم الإسلامية"""
    name: str
    arabic_name: str
    category: ConceptCategory
    definition: str
    cultural_context: str
    historical_background: str
    practical_application: str
    related_concepts: List[str]
    sources: List[str]
    examples: List[str]
    common_misconceptions: List[str]

class IslamicContextExplainer:
    """شارح السياق الثقافي الإسلامي"""
    
    def __init__(self):
        """تهيئة قاعدة المعرفة الإسلامية"""
        self.concepts_database = self._initialize_concepts_database()
        self.search_keywords = self._build_search_index()
    
    def _initialize_concepts_database(self) -> Dict[str, IslamicConcept]:
        """إنشاء قاعدة بيانات المفاهيم الإسلامية"""
        concepts = {}
        
        # مفاهيم العبادات
        concepts["salah"] = IslamicConcept(
            name="الصلاة",
            arabic_name="الصلاة",
            category=ConceptCategory.WORSHIP,
            definition="الصلاة هي الركن الثاني من أركان الإسلام، وهي عبادة بدنية وروحية تؤدى خمس مرات في اليوم",
            cultural_context="الصلاة تمثل محور الحياة الإسلامية اليومية، حيث تنظم الوقت وتربط المسلم بربه والمجتمع المسلم",
            historical_background="فُرضت الصلاة في رحلة الإسراء والمعراج، وكانت في البداية خمسين صلاة ثم خففت إلى خمس بنفس الأجر",
            practical_application="تؤدى الصلاة في المسجد جماعة أو في أي مكان طاهر، مع استقبال القبلة والطهارة",
            related_concepts=["وضوء", "قبلة", "أذان", "إمامة", "جماعة"],
            sources=["القرآن الكريم", "السنة النبوية", "إجماع العلماء"],
            examples=["صلاة الفجر قبل الشروق", "صلاة الجمعة الجماعية", "قصر الصلاة في السفر"],
            common_misconceptions=["أن الصلاة مجرد حركات جسدية", "أن الصلاة تكفي عن العمل الصالح"]
        )
        
        concepts["hajj"] = IslamicConcept(
            name="الحج",
            arabic_name="الحج",
            category=ConceptCategory.WORSHIP,
            definition="الحج هو الركن الخامس من أركان الإسلام، وهو زيارة البيت الحرام في مكة لأداء مناسك معينة",
            cultural_context="الحج يوحد المسلمين من جميع أنحاء العالم في تجربة روحية واحدة، ويكسر الحواجز العرقية والطبقية",
            historical_background="الحج سنة إبراهيمية قديمة، أعاد الإسلام إحياءها وتنظيمها، وهو واجب مرة في العمر لمن استطاع",
            practical_application="يؤدى الحج في أشهر معينة بمناسك محددة تشمل الطواف والسعي والوقوف بعرفة",
            related_concepts=["عمرة", "طواف", "سعي", "عرفة", "إحرام"],
            sources=["القرآن الكريم", "السنة النبوية", "كتب المناسك"],
            examples=["طواف الوداع", "الوقوف بعرفة", "رمي الجمرات"],
            common_misconceptions=["أن الحج مجرد سياحة دينية", "أن العمرة تغني عن الحج"]
        )
        
        concepts["jihad"] = IslamicConcept(
            name="الجهاد",
            arabic_name="الجهاد",
            category=ConceptCategory.JURISPRUDENCE,
            definition="الجهاد لغة البذل والمشقة، وشرعاً بذل الجهد في سبيل الله بأشكال مختلفة",
            cultural_context="مفهوم الجهاد يشمل جهاد النفس والمجتمع والدفاع، وليس مقصوراً على القتال",
            historical_background="الجهاد في الإسلام له ضوابط شرعية صارمة وأهداف محددة لحماية الدين والمجتمع",
            practical_application="يشمل جهاد النفس عن المعاصي، والجهاد بالعلم والدعوة، والدفاع عن المظلومين",
            related_concepts=["جهاد النفس", "الأمر بالمعروف", "النهي عن المنكر", "الدفاع"],
            sources=["القرآن الكريم", "السنة النبوية", "كتب الفقه"],
            examples=["طلب العلم جهاد", "الإحسان للوالدين جهاد", "العمل الصالح جهاد"],
            common_misconceptions=["أن الجهاد يعني القتال فقط", "أن الجهاد لا ضوابط له"]
        )
        
        # مفاهيم العقائد
        concepts["tawhid"] = IslamicConcept(
            name="التوحيد",
            arabic_name="التوحيد",
            category=ConceptCategory.BELIEFS,
            definition="التوحيد هو إفراد الله بالعبادة والاعتقاد بوحدانيته في ذاته وصفاته وأفعاله",
            cultural_context="التوحيد أساس العقيدة الإسلامية ومنطلق كل التصورات والقيم في الحياة الإسلامية",
            historical_background="دعوة جميع الأنبياء كانت للتوحيد، والإسلام خاتم الأديان في تقرير هذا المبدأ",
            practical_application="يظهر التوحيد في العبادة والأخلاق والمعاملات وكل جوانب الحياة",
            related_concepts=["شهادة أن لا إله إلا الله", "أسماء الله الحسنى", "صفات الله"],
            sources=["القرآن الكريم", "السنة النبوية", "كتب العقيدة"],
            examples=["لا إله إلا الله", "الدعاء لله وحده", "التوكل على الله"],
            common_misconceptions=["أن التوحيد مجرد كلمة تقال", "الخلط بين التوحيد والتوسل"]
        )
        
        # مفاهيم الأخلاق
        concepts["ihsan"] = IslamicConcept(
            name="الإحسان",
            arabic_name="الإحسان",
            category=ConceptCategory.ETHICS,
            definition="الإحسان هو أعلى مراتب الدين، وهو أن تعبد الله كأنك تراه فإن لم تكن تراه فإنه يراك",
            cultural_context="الإحسان يمثل الكمال الأخلاقي والروحي في الإسلام، ويشمل الإتقان في كل عمل",
            historical_background="الإحسان مفهوم قرآني ونبوي يدعو للتميز والإتقان في العبادة والمعاملة",
            practical_application="يظهر الإحسان في إتقان العمل، وحسن المعاملة، والصدق في العبادة",
            related_concepts=["تقوى", "مراقبة الله", "إتقان", "تزكية"],
            sources=["حديث جبريل", "القرآن الكريم", "كتب التصوف"],
            examples=["الإحسان في العمل", "الإحسان للوالدين", "الإحسان في العبادة"],
            common_misconceptions=["أن الإحسان مقصور على العبادة", "أن الإحسان يعني التساهل"]
        )
        
        return concepts
    
    def _build_search_index(self) -> Dict[str, List[str]]:
        """بناء فهرس البحث للكلمات المفتاحية"""
        index = {}
        
        for concept_id, concept in self.concepts_database.items():
            # إضافة الاسم والاسم العربي
            keywords = [concept.name.lower(), concept.arabic_name.lower()]
            
            # إضافة المفاهيم المترابطة
            keywords.extend([related.lower() for related in concept.related_concepts])
            
            # إضافة كلمات من التعريف
            definition_words = re.findall(r'\b\w+\b', concept.definition.lower())
            keywords.extend(definition_words)
            
            for keyword in keywords:
                if keyword not in index:
                    index[keyword] = []
                if concept_id not in index[keyword]:
                    index[keyword].append(concept_id)
        
        return index
    
    def search_concepts(self, query: str) -> List[str]:
        """البحث عن المفاهيم بناءً على الاستعلام"""
        query_words = re.findall(r'\b\w+\b', query.lower())
        concept_scores = {}
        
        for word in query_words:
            # البحث المباشر
            if word in self.search_keywords:
                for concept_id in self.search_keywords[word]:
                    concept_scores[concept_id] = concept_scores.get(concept_id, 0) + 3
            
            # البحث الجزئي
            for keyword, concept_ids in self.search_keywords.items():
                if word in keyword or keyword in word:
                    for concept_id in concept_ids:
                        concept_scores[concept_id] = concept_scores.get(concept_id, 0) + 1
        
        # ترتيب النتائج حسب النقاط
        sorted_concepts = sorted(concept_scores.items(), key=lambda x: x[1], reverse=True)
        return [concept_id for concept_id, score in sorted_concepts[:5]]
    
    def explain_concept(self, concept_id: str, detail_level: str = "medium") -> str:
        """شرح مفهوم إسلامي بمستوى تفصيل محدد"""
        if concept_id not in self.concepts_database:
            return "المفهوم غير موجود في قاعدة البيانات."
        
        concept = self.concepts_database[concept_id]
        
        explanation = f"🕌 **{concept.arabic_name}** ({concept.category.value})\n\n"
        
        # التعريف الأساسي
        explanation += f"📖 **التعريف:**\n{concept.definition}\n\n"
        
        if detail_level in ["medium", "detailed"]:
            # السياق الثقافي
            explanation += f"🌍 **السياق الثقافي:**\n{concept.cultural_context}\n\n"
            
            # التطبيق العملي
            explanation += f"⚡ **التطبيق العملي:**\n{concept.practical_application}\n\n"
            
            # أمثلة
            if concept.examples:
                explanation += f"📝 **أمثلة:**\n"
                for example in concept.examples[:3]:
                    explanation += f"• {example}\n"
                explanation += "\n"
        
        if detail_level == "detailed":
            # الخلفية التاريخية
            explanation += f"📜 **الخلفية التاريخية:**\n{concept.historical_background}\n\n"
            
            # المفاهيم المترابطة
            if concept.related_concepts:
                explanation += f"🔗 **مفاهيم مترابطة:**\n"
                for related in concept.related_concepts[:5]:
                    explanation += f"• {related}\n"
                explanation += "\n"
            
            # المفاهيم الخاطئة الشائعة
            if concept.common_misconceptions:
                explanation += f"⚠️ **مفاهيم خاطئة شائعة:**\n"
                for misconception in concept.common_misconceptions:
                    explanation += f"• {misconception}\n"
                explanation += "\n"
            
            # المصادر
            if concept.sources:
                explanation += f"📚 **المصادر:**\n"
                for source in concept.sources:
                    explanation += f"• {source}\n"
        
        return explanation.strip()
    
    def get_interactive_menu(self, concept_id: str) -> str:
        """إنشاء قائمة تفاعلية لاستكشاف المفهوم"""
        if concept_id not in self.concepts_database:
            return "المفهوم غير موجود."
        
        concept = self.concepts_database[concept_id]
        
        menu = f"🔍 **استكشاف مفهوم: {concept.arabic_name}**\n\n"
        menu += "اختر ما تريد معرفته:\n\n"
        menu += "1️⃣ التعريف الأساسي\n"
        menu += "2️⃣ السياق الثقافي\n"
        menu += "3️⃣ الخلفية التاريخية\n"
        menu += "4️⃣ التطبيق العملي\n"
        menu += "5️⃣ أمثلة من الواقع\n"
        menu += "6️⃣ المفاهيم المترابطة\n"
        menu += "7️⃣ المفاهيم الخاطئة الشائعة\n"
        menu += "8️⃣ الشرح الكامل\n\n"
        menu += "أرسل الرقم المطلوب أو اكتب سؤالك."
        
        return menu
    
    def get_concept_aspect(self, concept_id: str, aspect: str) -> str:
        """الحصول على جانب محدد من المفهوم"""
        if concept_id not in self.concepts_database:
            return "المفهوم غير موجود."
        
        concept = self.concepts_database[concept_id]
        
        aspects = {
            "1": f"📖 **التعريف:**\n{concept.definition}",
            "2": f"🌍 **السياق الثقافي:**\n{concept.cultural_context}",
            "3": f"📜 **الخلفية التاريخية:**\n{concept.historical_background}",
            "4": f"⚡ **التطبيق العملي:**\n{concept.practical_application}",
            "5": f"📝 **أمثلة:**\n" + "\n".join([f"• {ex}" for ex in concept.examples]),
            "6": f"🔗 **مفاهيم مترابطة:**\n" + "\n".join([f"• {rel}" for rel in concept.related_concepts]),
            "7": f"⚠️ **مفاهيم خاطئة شائعة:**\n" + "\n".join([f"• {misc}" for misc in concept.common_misconceptions]),
            "8": self.explain_concept(concept_id, "detailed")
        }
        
        return aspects.get(aspect, "اختيار غير صحيح. يرجى اختيار رقم من 1 إلى 8.")
    
    def get_random_concept(self) -> str:
        """الحصول على مفهوم عشوائي للتعلم"""
        import random
        concept_id = random.choice(list(self.concepts_database.keys()))
        concept = self.concepts_database[concept_id]
        
        return f"💡 **مفهوم اليوم: {concept.arabic_name}**\n\n{concept.definition}\n\nهل تريد معرفة المزيد؟ اكتب 'شرح {concept.arabic_name}'"
    
    def get_category_concepts(self, category: ConceptCategory) -> List[str]:
        """الحصول على المفاهيم حسب التصنيف"""
        concepts = []
        for concept_id, concept in self.concepts_database.items():
            if concept.category == category:
                concepts.append(f"• {concept.arabic_name}")
        return concepts
    
    def suggest_related_concepts(self, current_concept_id: str) -> str:
        """اقتراح مفاهيم مترابطة"""
        if current_concept_id not in self.concepts_database:
            return "المفهوم غير موجود."
        
        concept = self.concepts_database[current_concept_id]
        suggestions = []
        
        for related_name in concept.related_concepts[:3]:
            # البحث عن المفهوم المترابط في قاعدة البيانات
            for concept_id, other_concept in self.concepts_database.items():
                if other_concept.arabic_name.lower() == related_name.lower():
                    suggestions.append(f"• {related_name} - {other_concept.definition[:50]}...")
                    break
            else:
                suggestions.append(f"• {related_name}")
        
        if suggestions:
            return f"🔗 **مفاهيم قد تهمك:**\n\n" + "\n".join(suggestions)
        else:
            return "لا توجد مفاهيم مترابطة متاحة حالياً."