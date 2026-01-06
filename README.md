# Model Context Protocol Demonstration

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![LangChain](https://img.shields.io/badge/langchain-%231C3C3C.svg?style=for-the-badge&logo=langchain&logoColor=white)
![Ollama](https://img.shields.io/badge/ollama-%23000000.svg?style=for-the-badge&logo=ollama&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![uv](https://img.shields.io/badge/uv-%23DE5FE9.svg?style=for-the-badge&logo=uv&logoColor=white)


The purpose of this repository was a hands on presentation of the Model Context Protocol (MCP) capabilities, showcasing local MCP servers from a locally running Model to handle interacting with a Web API (`blog`, `gmail`) and vector database (`rag`). Multiple Agent pipelines are built to handle task orchestration (`agents`).

Each MCP server can be attached to vscode, or a TUI can be started for an interactive chat. The chat allows queries such as "summarize my note on 'x' and post it to my blog, then update my mailing list with a notification for the new post" to trigger a full task pipeline. 

`Agentic Workflows.pdf` is a full write-up and explanation of MCP and common agentic pipelines.
