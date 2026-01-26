from .base import BaseAgent
from ..models.state import SharedState
from ..utils.llm_client import LLMClient

class DocumentationAgent(BaseAgent):
    def __init__(self, state: SharedState, llm: LLMClient):
        super().__init__("Documentation", state, llm)
        
    async def run(self):
        # In a real system, this might generate a PDF or a Markdown report via LLM
        # Here we just print the final report to console for the user
        self.log("Action", "Compiling final report")
        
        formula = self.state.current_formula
        brief = self.state.brief
        risks = self.state.stability_risks
        
        report = []
        report.append(f"# Formulation Report: {formula.name}")
        report.append(f"**Target Application:** {brief.product_type} for {brief.target_audience}")
        report.append(f"**Form:** {formula.form} | **pH:** {formula.ph_target} | **Viscosity:** {formula.viscosity_target}")
        
        report.append("\n## Formula Table")
        report.append("| Phase | Ingredient | % | Function | Justification |")
        report.append("|-------|------------|---|----------|---------------|")
        
        # Sort by Phase
        sorted_ingredients = sorted(formula.ingredients, key=lambda x: x.phase)
        ingredients_dict = [i.model_dump() for i in sorted_ingredients]
        
        for ing in ingredients_dict:
            report.append(f"| {ing['phase']} | {ing['name']} | {ing['percentage']}% | {ing['function']} | {ing['justification']} |")
            
        report.append(f"| | **TOTAL** | **{formula.total_percentage}%** | | |")
        
        if risks:
            report.append("\n## Stability Risk Assessment")
            for risk in risks:
                report.append(f"- **[{risk.risk_level.upper()}] {risk.category}**: {risk.description}")
                report.append(f"  *Mitigation:* {risk.mitigation_strategy}")
        
        report.append("\n## References")
        for ev in self.state.evidence_pool:
            report.append(f"- {ev.citation}")

        final_output = "\n".join(report)
        print("\n" + "="*50)
        print(final_output)
        print("="*50 + "\n")
        
        self.state.meta_memory["final_report"] = final_output
        self.log("Result", "Report generated")
