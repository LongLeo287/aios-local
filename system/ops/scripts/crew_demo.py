import os
import sys

# ==========================================
# Cáº¥u hÃ¬nh Local LLM cho CrewAI (cháº¡y 100% Offline qua Ollama)
# ==========================================
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_API_KEY"] = "ollama"
os.environ["OPENAI_MODEL_NAME"] = "gemma2:2b"

# Import Library vÃ  AI OS Tools
sys.path.append(os.environ.get("AOS_ROOT", "."))
from crewai import Agent, Task, Crew, Process
from plugins.crewai_tools_bridge import GitingestTool, LightRAGTool

def run_crew():
    print("ðŸš€ [PHASE 4] Khá»Ÿi cháº¡y Äá»™i NhÃ³m: AI OS Multi-Agent Sync")
    print("----------------------------------------------------------")

    # 1. Khá»Ÿi táº¡o vÅ© khÃ­ (Tools) tá»« AI OS
    git_tool = GitingestTool()
    rag_tool = LightRAGTool()

    # 2. Khai bÃ¡o NhÃ¢n Sá»± (Agents)
    analyst = Agent(
        role="NhÃ  PhÃ¢n TÃ­ch MÃ£ Nguá»“n (Code_Analyst)",
        goal="Äá»c mÃ£ nguá»“n Repo Github báº±ng Gitingest (GitNexus) vÃ  tÃ³m táº¯t cáº¥u trÃºc.",
        backstory="Báº¡n lÃ  chuyÃªn gia Ä‘á»c code nhanh. Nhiá»‡m vá»¥ cá»§a báº¡n lÃ  dÃ¹ng Gitingest Tool hÃºt source code vá» vÃ  viáº¿t 1 báº£n tÃ³m táº¯t máº¡ch láº¡c Ä‘á»ƒ bÃ n giao cho Kiáº¿n trÃºc sÆ°.",
        tools=[git_tool],
        allow_delegation=False,
        verbose=True
    )

    architect = Agent(
        role="Kiáº¿n TrÃºc SÆ° Tri Thá»©c (Knowledge_Architect)",
        goal="Sá»­ dá»¥ng LightRAG quÃ©t vÃ  nÃ©n bÃ¡o cÃ¡o cá»§a nhÃ¢n viÃªn Analyst vÃ o Äá»“ thá»‹ tri thá»©c.",
        backstory="Báº¡n lÃ  ngÆ°á»i canh giá»¯ ThÆ° viá»‡n AI OS. Báº¡n khÃ´ng phÃ¢n tÃ­ch code, báº¡n chá»‰ chá» nháº­n bÃ¡o cÃ¡o (Context) tá»« Analyst vÃ  thá»±c thi thao tÃ¡c Insert vÃ o LightRAG Pipeline.",
        tools=[rag_tool],
        allow_delegation=False,
        verbose=True
    )

    # 3. PhÃ¢n cÃ´ng CÃ´ng viá»‡c (Tasks)
    task_code = Task(
        description="DÃ¹ng cÃ´ng cá»¥ Gitingest, hÃ£y ingest vÃ  phÃ¢n tÃ­ch Repository nÃ y: 'https://github.com/carlrannaberg/ccpoke'. TÃ³m táº¯t láº¡i nÃ³ dÃ¹ng Ä‘á»ƒ lÃ m gÃ¬ vÃ  cÃ´ng nghá»‡ gÃ¬.",
        expected_output="1 BÃ i bÃ¡o cÃ¡o ngáº¯n (dÆ°á»›i 300 chá»¯) tÃ³m lÆ°á»£c Repo.",
        agent=analyst
    )

    task_index = Task(
        description="Call cÃ´ng cá»¥ LightRAG Tool Ä‘á»ƒ náº¡p bÃ i bÃ¡o cÃ¡o cá»§a Code Analyst vÃ o Graph RAG Database. Náº¿u insert thÃ nh cÃ´ng hÃ£y bÃ¡o cÃ¡o.",
        expected_output="Tin nháº¯n xÃ¡c nháº­n hoÃ n thÃ nh cÃ´ng viá»‡c náº¡p Data.",
        agent=architect,
        context=[task_code]
    )

    # 4. Láº¯p rÃ¡p Äá»™i nhÃ³m (Crew)
    ai_os_crew = Crew(
        agents=[analyst, architect],
        tasks=[task_code, task_index],
        process=Process.sequential,
        verbose=True
    )

    # Gá»i hÃ m Thá»±c thi
    result = ai_os_crew.kickoff()

    print("\nðŸ Káº¾T QUáº¢ CUá»I CÃ™NG Tá»ª Äá»˜I NHÃ“M:")
    print("===================================")
    print(result)
    print("===================================")

if __name__ == "__main__":
    run_crew()

