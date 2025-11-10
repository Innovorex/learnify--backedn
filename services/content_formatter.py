"""
Universal Content Formatter for AI Tutor
=========================================
Formats raw content into structured educational format for ANY subject.

Works with:
- CBSE textbook content (Mathematics, Science, Social Studies, Languages, etc.)
- State board syllabus
- Uploaded teaching materials (PDFs, documents)
"""

from typing import Dict, List, Optional
import re


class ContentFormatter:
    """
    Universal content formatter that structures educational content
    for comprehensive topic overviews across all subjects.
    """

    def __init__(self):
        self.subject_keywords = {
            "mathematics": ["theorem", "formula", "equation", "proof", "example", "solution"],
            "science": ["experiment", "observation", "activity", "chemical equation", "reaction", "process"],
            "social_studies": ["historical event", "timeline", "civilization", "culture", "geography"],
            "languages": ["grammar rule", "vocabulary", "example sentence", "usage", "meaning"]
        }

    def format_comprehensive_overview(
        self,
        raw_content: str,
        topic_name: str,
        subject: str = "General",
        grade: str = "10",
        is_uploaded_material: bool = False
    ) -> str:
        """
        Creates a structured, comprehensive overview prompt that instructs
        the LLM to format content properly.

        This returns a PROMPT that tells the LLM how to structure the response.

        Args:
            raw_content: The full text content
            topic_name: Topic name (for CBSE) or material title (for uploads)
            subject: Subject for context
            grade: Grade for context
            is_uploaded_material: If True, uses material analysis format
        """

        # For uploaded materials, use special analysis format
        if is_uploaded_material:
            return self._format_uploaded_material_prompt(raw_content, subject, grade)

        # Detect subject type for customized formatting (CBSE content)
        subject_lower = subject.lower()

        if "math" in subject_lower:
            return self._format_mathematics_prompt(raw_content, topic_name, grade)
        elif "science" in subject_lower or "physics" in subject_lower or "chemistry" in subject_lower or "biology" in subject_lower:
            return self._format_science_prompt(raw_content, topic_name, grade)
        elif "social" in subject_lower or "history" in subject_lower or "geography" in subject_lower:
            return self._format_social_studies_prompt(raw_content, topic_name, grade)
        else:
            return self._format_general_prompt(raw_content, topic_name, grade)

    def _format_mathematics_prompt(self, content: str, topic: str, grade: str) -> str:
        """Format for Mathematics topics"""
        return f"""You are an AI Teaching Assistant for Grade {grade} Mathematics.

TASK: Provide a COMPREHENSIVE, STRUCTURED overview of "{topic}"

TEXTBOOK CONTENT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{content}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REQUIRED FORMAT:

{topic}

Introduction
• [2-3 sentences overview of the topic]
• [Key focus areas of this chapter/topic]
• [Why this topic is important]

[Main Concept/Section 1 Name]
• [Key concept 1 with clear explanation]
• [Key concept 2]
• Formula: [if applicable - use proper notation]
• Used for: [practical applications]
• Important note: [any critical points]

[Main Concept/Section 2 Name]
• [Detailed explanation]
• [Key properties or rules]

Theorems and Definitions (if applicable)
Theorem X.Y: [Name of theorem]
• Statement: [Formal mathematical statement]
• Explanation: [What it means in simple terms]
• Application: [How it's used]

Examples and Applications
Example 1: [Problem statement]
• Problem: [Clear problem description]
• Solution:
  - Step 1: [First step with explanation]
  - Step 2: [Second step with explanation]
  - Answer: [Final answer]

Example 2: [Another problem]
[Follow same structure]

Key Formulas Summary
• Formula 1: a = bq + r (where 0 ≤ r < b)
• Formula 2: HCF × LCM = a × b
• [List all important formulas from the content]

Important Points to Remember
• [Key point 1 that students should remember]
• [Key point 2]
• [Common mistakes to avoid]

Teaching Tips
• [Practical tip 1 for teachers - e.g., use visual aids]
• [Tip 2 - e.g., common student difficulties and how to address them]
• [Tip 3 - e.g., engaging activities or real-world examples]
• [Tip 4 - e.g., assessment strategies]

CRITICAL RULES:
1. Use ONLY the textbook content provided above
2. Include ALL major concepts, theorems, and examples from the content
3. Format with clear sections using bullet points (•)
4. Include specific formulas with proper mathematical notation
5. Provide concrete examples with step-by-step solutions exactly as shown in content
6. End with practical teaching tips
7. Be comprehensive - this is the complete introduction to the topic
8. If content mentions page numbers or figure numbers, include them
9. Maintain the exact mathematical notation from the textbook
10. Keep the same level of detail and rigor as the original content
"""

    def _format_science_prompt(self, content: str, topic: str, grade: str) -> str:
        """Format for Science topics (Physics, Chemistry, Biology)"""
        return f"""You are an AI Teaching Assistant for Grade {grade} Science.

TASK: Provide a COMPREHENSIVE, STRUCTURED overview of "{topic}"

TEXTBOOK/MATERIAL CONTENT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{content}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REQUIRED FORMAT:

{topic}

Introduction
• [2-3 sentences overview]
• [What students will learn in this topic]
• [Real-world relevance]

[Main Concept 1]
• [Detailed explanation of the concept]
• [Key characteristics or properties]
• Definition: [If applicable]
• Examples: [Real-world or textbook examples]

[Main Concept 2]
• [Content]

Types/Classifications (if applicable)
1. [Type 1 Name]
   • [Description]
   • Example: [Specific example]

2. [Type 2 Name]
   • [Description]
   • Example: [Specific example]

Chemical Reactions/Equations (if applicable)
Reaction 1: [Name of reaction]
• Equation: [Chemical equation with proper notation]
  Example: Mg + O₂ → MgO
• Observation: [What happens during the reaction]
• Explanation: [Why this happens]

Reaction 2: [Name]
[Follow same structure]

Activities/Experiments
Activity X.Y: [Name/Description]
• Procedure: [Brief procedure steps]
• Observation: [What is observed]
• Inference: [What this tells us]
• Safety note: [If applicable]

Indicators of [Process/Change] (if applicable)
• Indicator 1: [Description]
• Indicator 2: [Description]
• [List all indicators mentioned]

Examples from Daily Life
• Example 1: [Everyday example with explanation]
• Example 2: [Another example]
• [Show how the concept applies in real life]

Prevention/Applications (if applicable)
• [How to prevent unwanted effects]
• [How to use this knowledge]
• [Practical applications]

Key Points to Remember
• [Critical concept 1]
• [Critical concept 2]
• [Important distinctions or comparisons]

Teaching Tips
• [Demonstration ideas or experiments]
• [Common misconceptions to address]
• [Visual aids that would help]
• [Questions to ask students to check understanding]
• [Safety considerations if doing experiments]

CRITICAL RULES:
1. Use ONLY the content provided above
2. Include ALL activities, experiments, and examples from the content
3. Write chemical equations with proper notation (use subscripts/superscripts appropriately)
4. Format with clear sections and bullet points (•)
5. Include observations and inferences from activities
6. Connect concepts to daily life examples
7. End with practical teaching tips
8. Be comprehensive and detailed
9. Preserve exact terminology from the textbook
10. If content mentions figures or activities by number, include them
"""

    def _format_social_studies_prompt(self, content: str, topic: str, grade: str) -> str:
        """Format for Social Studies topics"""
        return f"""You are an AI Teaching Assistant for Grade {grade} Social Studies.

TASK: Provide a COMPREHENSIVE, STRUCTURED overview of "{topic}"

TEXTBOOK CONTENT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{content}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REQUIRED FORMAT:

{topic}

Introduction
• [Overview of the topic]
• [Historical/geographical context]
• [Why this topic is significant]

[Main Section 1]
• [Detailed content]
• [Key events, facts, or concepts]
• [Important dates, places, or figures]

[Main Section 2]
• [Content]

Key Events/Timeline (if applicable)
• [Year/Period]: [Event and its significance]
• [Year/Period]: [Event and significance]

Important Concepts
• [Concept 1]: [Explanation]
• [Concept 2]: [Explanation]

Causes and Effects (if applicable)
Causes:
• [Cause 1]
• [Cause 2]

Effects:
• [Effect 1]
• [Effect 2]

Key Figures/Places
• [Name/Place]: [Brief description and importance]
• [Name/Place]: [Description]

Examples and Case Studies
• [Example 1 with context]
• [Example 2]

Connections to Today
• [How this topic relates to current times]
• [Why it matters for students to understand this]

Teaching Tips
• [Discussion questions to engage students]
• [Activities or projects related to the topic]
• [Visual aids like maps, timelines, or images to use]
• [Ways to make the content relatable]

CRITICAL RULES:
1. Use ONLY the content provided
2. Include all key events, dates, figures, and places
3. Format with clear sections and bullet points
4. Provide historical/geographical context
5. Make connections to contemporary relevance
6. Be comprehensive and factually accurate
7. End with teaching tips
"""

    def _format_general_prompt(self, content: str, topic: str, grade: str) -> str:
        """Format for general topics or other subjects"""
        return f"""You are an AI Teaching Assistant for Grade {grade}.

TASK: Provide a COMPREHENSIVE, STRUCTURED overview of "{topic}"

CONTENT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{content}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REQUIRED FORMAT:

{topic}

Introduction
• [Overview of the topic]
• [What students will learn]
• [Why this is important]

[Main Section 1]
• [Detailed explanation]
• [Key concepts or points]
• Examples: [If applicable]

[Main Section 2]
• [Content]

Key Definitions (if applicable)
• [Term 1]: [Definition]
• [Term 2]: [Definition]

Examples and Illustrations
• Example 1: [Description]
• Example 2: [Description]

Important Points to Remember
• [Key point 1]
• [Key point 2]

Applications/Usage (if applicable)
• [How this is used or applied]
• [Practical examples]

Teaching Tips
• [Suggested teaching approaches]
• [Common challenges and how to address them]
• [Activities or exercises]
• [Assessment ideas]

CRITICAL RULES:
1. Use ONLY the content provided above
2. Include ALL major concepts and examples from the content
3. Format with clear sections and bullet points (•)
4. Be comprehensive and detailed
5. End with practical teaching tips
6. Preserve exact terminology and concepts from the source
"""

    def _format_uploaded_material_prompt(self, content: str, subject: str, grade: str) -> str:
        """
        Format for uploaded materials (PDFs, documents).
        This analyzes the ENTIRE material and extracts all topics/sections.
        Grade and subject are ignored - we analyze the content directly.
        """
        return f"""You are an AI Teaching Assistant analyzing uploaded teaching material.

TASK: READ, PARSE, and EXPLAIN ALL content from the uploaded PDF/document below.

UPLOADED MATERIAL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{content}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CRITICAL INSTRUCTIONS:

1. READ the entire uploaded material above carefully
2. PARSE and IDENTIFY all topics, sections, chapters, and concepts in the material
3. EXPLAIN each topic found in the material, topic by topic, in detail
4. Extract information directly from the material - don't make assumptions
5. DO NOT ask for clarification or more information
6. DO NOT mention grade, subject, or topic name unless it's in the material
7. Work with whatever content is provided

REQUIRED FORMAT:

Material Analysis

Introduction
• [What this material covers - based on analyzing the content]
• [Subject/topic identified from the material itself]
• [Grade level if mentioned in the material]
• [Main learning objectives found in the material]

[Section/Topic 1 - Name extracted from material]
• [Full explanation of this topic from the material]
• [All key concepts covered in this section]
• [Important definitions, formulas, or principles]
• [Examples or illustrations if provided]

[Section/Topic 2 - Name extracted from material]
• [Complete explanation from material]
• [Key concepts]
• [Important points]

[Section/Topic 3 - Name extracted from material]
• [Content from material]

[Continue for ALL sections/topics found in the material]

Key Concepts Summary
• [Every major concept from the material]
• [Important terms and definitions]
• [Critical formulas or principles]

Examples and Applications (if present)
• [Example 1 from material with full explanation]
• [Example 2 from material]
• [Practical applications mentioned]

Important Points to Remember
• [Key point 1 from material]
• [Key point 2 from material]
• [Critical information students must know]

Teaching Tips
• [How to teach these concepts effectively]
• [Suggested activities based on the content]
• [Common challenges students face with this content]
• [Assessment strategies]

CRITICAL RULES:
1. Extract and explain EVERY topic, section, and concept found in the material
2. Use ONLY the uploaded material - no external information
3. Format with clear sections using bullet points (•)
4. Be comprehensive - don't skip any part of the material
5. If material has formulas/equations - explain them fully
6. If material has diagrams/figures - describe what they show
7. If material has activities/experiments - include all steps
8. Organize the content logically even if the original PDF is poorly structured
9. DO NOT ask clarifying questions - analyze what's there
10. Give detailed explanations for each topic extracted from the material
"""

    def format_followup_prompt(
        self,
        topic_name: str,
        relevant_content: str,
        user_question: str,
        conversation_history: List[Dict],
        subject: str = "General"
    ) -> str:
        """
        Creates a focused prompt for follow-up questions.
        Uses minimal context for fast responses.
        """

        # Get last 2 conversation turns (4 messages)
        recent_history = conversation_history[-4:] if len(conversation_history) > 4 else conversation_history
        history_text = ""

        for msg in recent_history:
            role = "Teacher" if msg['role'] == "user" else "AI"
            content = msg['content'][:200]  # Truncate for brevity
            history_text += f"\n{role}: {content}...\n"

        return f"""You are an AI Teaching Assistant for {subject}.

TOPIC: {topic_name}

RELEVANT CONTENT FOR THIS QUESTION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{relevant_content}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECENT CONVERSATION:
{history_text}

CURRENT QUESTION: {user_question}

INSTRUCTIONS:
1. Answer the specific question based on the relevant content above
2. Be clear, detailed, and educational
3. Reference specific parts of the content when answering
4. If the question asks about something NOT in the content, say: "This specific aspect is not covered in the current material."
5. Use bullet points for clarity
6. Provide examples if available in the content
7. Keep your answer focused and relevant to the question

Provide your answer:
"""


# Utility function to get content formatter
_formatter_instance = None

def get_content_formatter() -> ContentFormatter:
    """Get singleton instance of ContentFormatter"""
    global _formatter_instance
    if _formatter_instance is None:
        _formatter_instance = ContentFormatter()
    return _formatter_instance
