#!/usr/bin/env python3
"""
Prompt Refinement Module for Workflow Creator V3

Implements dual-pass prompt refinement:
1. Phase 2.5: Refine user request before requirements gathering
2. Phase 6: Refine generation agent prompts before execution

Uses prompt-redefiner skill for quality analysis and optimization.
"""

import json
import re
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class RefinementResult:
    """Result of prompt refinement"""
    original_prompt: str
    refined_prompt: str
    original_quality: int
    refined_quality: int
    improvements: List[str]
    persona_score: int
    hallucination_risk: int
    structural_clarity: int


class PromptRefiner:
    """Dual-pass prompt refinement using prompt-redefiner skill"""

    def __init__(self):
        self.refinement_history = []

    def refine_user_request(self, request: str) -> RefinementResult:
        """
        Phase 2.5: Refine user's workflow creation request

        Applies prompt-redefiner analysis to:
        - Remove ineffective personas
        - Add structural specifications
        - Define success criteria
        - Reduce hallucination risk

        Args:
            request: Original user request for workflow creation

        Returns:
            RefinementResult with refined prompt and quality metrics
        """

        # Analyze original request
        analysis = self._analyze_prompt(request, context="workflow_creation")

        # Apply refinements
        refined = self._apply_refinements(request, analysis, is_user_request=True)

        result = RefinementResult(
            original_prompt=request,
            refined_prompt=refined['prompt'],
            original_quality=analysis['overall_quality'],
            refined_quality=refined['quality'],
            improvements=refined['improvements'],
            persona_score=analysis['persona_score'],
            hallucination_risk=analysis['hallucination_risk'],
            structural_clarity=refined['structural_clarity']
        )

        self.refinement_history.append({
            'phase': 'user_request',
            'result': result
        })

        return result

    def refine_agent_prompts(
        self,
        prompts: Dict[str, str],
        domain: str,
        format_config: Dict[str, Any]
    ) -> Dict[str, RefinementResult]:
        """
        Phase 6: Refine generation agent prompts before execution

        Optimizes prompts for:
        - Claude 4.5 explicit instructions
        - Parallel tool calling
        - Context-aware generation
        - XML structured output
        - Domain-specific patterns

        Args:
            prompts: Dict of agent_name -> prompt_text
            domain: Target domain (DevOps, Security, etc.)
            format_config: Workflow format configuration

        Returns:
            Dict of agent_name -> RefinementResult
        """

        refined_prompts = {}

        for agent_name, prompt in prompts.items():
            analysis = self._analyze_prompt(
                prompt,
                context="agent_generation",
                domain=domain
            )

            refined = self._apply_refinements(
                prompt,
                analysis,
                is_user_request=False,
                domain=domain,
                format_config=format_config
            )

            result = RefinementResult(
                original_prompt=prompt,
                refined_prompt=refined['prompt'],
                original_quality=analysis['overall_quality'],
                refined_quality=refined['quality'],
                improvements=refined['improvements'],
                persona_score=analysis['persona_score'],
                hallucination_risk=analysis['hallucination_risk'],
                structural_clarity=refined['structural_clarity']
            )

            refined_prompts[agent_name] = result

            self.refinement_history.append({
                'phase': 'agent_prompt',
                'agent': agent_name,
                'result': result
            })

        return refined_prompts

    def _analyze_prompt(
        self,
        prompt: str,
        context: str,
        domain: str = None
    ) -> Dict[str, int]:
        """Analyze prompt quality using prompt-redefiner patterns"""

        # Persona detection (from persona-prompt-optimizer)
        persona_patterns = {
            'expert': r'you are (an? )?(expert|specialist|professional)',
            'role': r'you are (an? )?(\w+) (who|that)',
            'low_knowledge': r'you are (an? )?(toddler|child|beginner|layperson)',
            'stylistic': r'(respond|write|speak) (in|like|as)',
            'perspective': r'(imagine|pretend|act as if)'
        }

        persona_score = 100
        detected_personas = []

        for persona_type, pattern in persona_patterns.items():
            if re.search(pattern, prompt.lower()):
                detected_personas.append(persona_type)
                if persona_type == 'low_knowledge':
                    persona_score = 0  # Harmful
                elif persona_type == 'expert':
                    persona_score = min(persona_score, 25)  # Ineffective
                elif persona_type == 'role':
                    persona_score = min(persona_score, 50)  # Ineffective

        # Hallucination risk assessment (from chain-of-verification)
        hallucination_risk = 50  # Default medium

        if context == "workflow_creation":
            # Workflow generation is prone to over-engineering
            hallucination_risk = 65
        elif context == "agent_generation":
            # Agent prompts prone to assumption-based implementation
            hallucination_risk = 60

        # Check for verification patterns
        if 'verify' in prompt.lower() or 'check' in prompt.lower():
            hallucination_risk -= 15

        # Check for list-based tasks (high risk)
        if re.search(r'(list|enumerate|identify all)', prompt.lower()):
            hallucination_risk += 20

        # Structural clarity assessment
        structural_clarity = 50

        if re.search(r'(objective|goal|purpose):', prompt.lower(), re.IGNORECASE):
            structural_clarity += 15

        if re.search(r'(success criteria|requirements|constraints):', prompt.lower(), re.IGNORECASE):
            structural_clarity += 15

        if re.search(r'(output format|deliverable|result):', prompt.lower(), re.IGNORECASE):
            structural_clarity += 10

        # Overall quality (weighted average)
        overall_quality = int(
            persona_score * 0.4 +
            (100 - hallucination_risk) * 0.4 +
            structural_clarity * 0.2
        )

        return {
            'persona_score': persona_score,
            'hallucination_risk': hallucination_risk,
            'structural_clarity': structural_clarity,
            'overall_quality': overall_quality,
            'detected_personas': detected_personas
        }

    def _apply_refinements(
        self,
        prompt: str,
        analysis: Dict[str, int],
        is_user_request: bool,
        domain: str = None,
        format_config: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Apply refinements based on analysis"""

        refined = prompt
        improvements = []

        # Remove ineffective personas
        if analysis['persona_score'] < 75:
            persona_patterns = [
                (r'you are (an? )?(expert|specialist|professional)[^\n]*\n?', ''),
                (r'you are (an? )?(\w+) (who|that)[^\n]*\n?', ''),
                (r'you are (an? )?(toddler|child|beginner|layperson)[^\n]*\n?', '')
            ]

            for pattern, replacement in persona_patterns:
                if re.search(pattern, refined, re.IGNORECASE):
                    refined = re.sub(pattern, replacement, refined, flags=re.IGNORECASE)
                    improvements.append("Removed ineffective persona")

        # Add structural specifications
        if analysis['structural_clarity'] < 70:
            if is_user_request:
                # Add workflow specification structure
                structural_additions = self._add_user_request_structure(refined, domain)
            else:
                # Add agent generation structure
                structural_additions = self._add_agent_structure(refined, domain, format_config)

            refined = structural_additions
            improvements.append("Added structural specifications")

        # Add success criteria
        if 'success' not in refined.lower():
            success_criteria = self._generate_success_criteria(refined, is_user_request, domain)
            refined += f"\n\n{success_criteria}"
            improvements.append("Defined success criteria")

        # Add verification protocol for high-risk tasks
        if analysis['hallucination_risk'] > 60 and 'verify' not in refined.lower():
            verification = self._add_verification_protocol(refined, is_user_request)
            refined += f"\n\n{verification}"
            improvements.append("Added verification protocol")

        # Add 2025 patterns for agent prompts
        if not is_user_request:
            refined = self._add_2025_patterns(refined, domain)
            improvements.append("Added 2025 best practices (parallel tools, XML, explicit)")

        # Recalculate quality
        new_analysis = self._analyze_prompt(refined, 'refined')

        return {
            'prompt': refined.strip(),
            'quality': new_analysis['overall_quality'],
            'structural_clarity': new_analysis['structural_clarity'],
            'improvements': improvements
        }

    def _add_user_request_structure(self, prompt: str, domain: str) -> str:
        """Add structure to user workflow request"""

        return f"""{prompt}

DELIVERABLE:
Claude Code skill ({domain or 'General'} domain) with:
- SKILL.md (workflow documentation)
- scripts/ (automation code)
- references/ (domain knowledge)

SUCCESS CRITERIA:
- Skill auto-triggers on relevant keywords
- Scripts are executable and under 200 lines each
- Validation passes (quick_validate.py)
- Installation succeeds

CONSTRAINTS:
- Do NOT over-engineer beyond stated requirements
- Do NOT add features not explicitly requested
- DO keep implementation focused and maintainable
"""

    def _add_agent_structure(
        self,
        prompt: str,
        domain: str,
        format_config: Dict[str, Any]
    ) -> str:
        """Add structure to agent generation prompt"""

        components = format_config.get('components', []) if format_config else []

        return f"""{prompt}

OBJECTIVE:
Generate production-ready {domain or 'workflow'} implementation

COMPONENTS:
{chr(10).join(f'- {comp}' for comp in components)}

CONSTRAINTS:
- Standard tools only (no custom dependencies unless necessary)
- Each script under 200 lines
- Follow 2025 Claude Code best practices
- Include proper YAML frontmatter

VERIFICATION:
1. Validate syntax (YAML, JSON, Python)
2. Check file structure completeness
3. Verify executable permissions
"""

    def _generate_success_criteria(
        self,
        prompt: str,
        is_user_request: bool,
        domain: str
    ) -> str:
        """Generate appropriate success criteria"""

        if is_user_request:
            return """SUCCESS CRITERIA:
- Workflow functions as specified
- All files generated and valid
- Validation passes
- Installation successful"""
        else:
            return """SUCCESS CRITERIA:
- All components generated
- Syntax validation passes
- Scripts are executable
- Documentation is complete"""

    def _add_verification_protocol(self, prompt: str, is_user_request: bool) -> str:
        """Add verification protocol to reduce hallucination risk"""

        if is_user_request:
            return """VERIFICATION PROTOCOL:
1. Check existing skills for similar implementations
2. Validate tool availability (MCP servers, npm packages)
3. Confirm file structure matches requirements
4. Test generated scripts"""
        else:
            return """VERIFICATION PROTOCOL:
1. Validate all file syntax
2. Check for missing dependencies
3. Verify output format correctness
4. Test with sample input"""

    def _add_2025_patterns(self, prompt: str, domain: str) -> str:
        """Add Claude 4.5 and 2025 best practices"""

        if '<use_parallel_tool_calls>' not in prompt:
            prompt += "\n\n<use_parallel_tool_calls>\nGenerate all independent files in parallel for speed.\n</use_parallel_tool_calls>"

        if '<default_to_action>' not in prompt:
            prompt += "\n\n<default_to_action>\nGenerate complete implementations immediately. Don't ask for confirmation.\n</default_to_action>"

        if '<context_aware_generation>' not in prompt:
            prompt += "\n\n<context_aware_generation>\nThis is a comprehensive generation task. Work systematically. Track context budget.\n</context_aware_generation>"

        if not re.search(r'<output_format>', prompt):
            prompt += """\n\n<output_format>
<generated_workflow>
  <files>
    <file path="..." language="...">content</file>
  </files>
</generated_workflow>
</output_format>"""

        return prompt

    def get_refinement_summary(self) -> Dict[str, Any]:
        """Get summary of all refinements performed"""

        user_refinements = [h for h in self.refinement_history if h['phase'] == 'user_request']
        agent_refinements = [h for h in self.refinement_history if h['phase'] == 'agent_prompt']

        return {
            'total_refinements': len(self.refinement_history),
            'user_request_refinements': len(user_refinements),
            'agent_prompt_refinements': len(agent_refinements),
            'avg_quality_improvement': sum(
                h['result'].refined_quality - h['result'].original_quality
                for h in self.refinement_history
            ) / len(self.refinement_history) if self.refinement_history else 0,
            'total_improvements': sum(
                len(h['result'].improvements)
                for h in self.refinement_history
            )
        }


if __name__ == '__main__':
    # Example usage
    refiner = PromptRefiner()

    # Phase 2.5: Refine user request
    user_request = "Create a CI/CD workflow for deploying to AWS"
    result1 = refiner.refine_user_request(user_request)

    print("=" * 60)
    print("PHASE 2.5: USER REQUEST REFINEMENT")
    print("=" * 60)
    print(f"Original Quality: {result1.original_quality}/100")
    print(f"Refined Quality: {result1.refined_quality}/100")
    print(f"Improvement: +{result1.refined_quality - result1.original_quality}")
    print(f"\nRefined Prompt:\n{result1.refined_prompt}")

    # Phase 6: Refine agent prompts
    agent_prompts = {
        'generation_agent': 'Generate a CI/CD workflow. Include best practices.'
    }

    results2 = refiner.refine_agent_prompts(
        agent_prompts,
        domain='DevOps',
        format_config={'components': ['SKILL.md', 'scripts/', 'references/']}
    )

    print("\n" + "=" * 60)
    print("PHASE 6: AGENT PROMPT REFINEMENT")
    print("=" * 60)
    for agent, result in results2.items():
        print(f"\nAgent: {agent}")
        print(f"Original Quality: {result.original_quality}/100")
        print(f"Refined Quality: {result.refined_quality}/100")
        print(f"Improvement: +{result.refined_quality - result.original_quality}")
        print(f"\nRefined Prompt:\n{result.refined_prompt[:200]}...")

    # Summary
    summary = refiner.get_refinement_summary()
    print("\n" + "=" * 60)
    print("REFINEMENT SUMMARY")
    print("=" * 60)
    print(json.dumps(summary, indent=2))
