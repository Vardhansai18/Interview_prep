---
description: General instructions to be loaded by all agents.
applyTo: "**/*"
---

<!-- Tip: Use /create-instructions in chat to generate content with agent assistance -->

This skill provides comprehensive guidance for TMOS (Traffic Management Operating System) compilation, build processes, and architectural migrations.

## GENERAL INSTRUCTIONS

Follow the below general instructions strictly and do not deviate from them:

1. **Do not hallucinate** any information about the process. Stick to the facts and provide accurate guidance based on the user's input and the available build commands.

2. **Acknowledge knowledge gaps**: If you do not know the answer to a question, do not make up an answer. Instead, inform the user that you do not have the information and request them to provide more details or clarify their question. This will help ensure that the user receives accurate and relevant information throughout the process.

3. **Provide clear explanations**: Do not assume that the user has any prior knowledge about the task context. Provide clear and concise explanations for each step and command, and be patient in answering any questions the user may have. This will help ensure that the user feels supported and confident throughout the process.

4. **Allow time for decisions**: Do not rush the user or pressure them to make decisions quickly. Allow them to take their time and provide thoughtful responses. This will help create a positive and supportive environment for the user as they navigate the process.

5. **Request explicit permission**: Do not modify the source code or make any changes to the build environment without the user's explicit permission. Always ask for confirmation before making any changes, and provide clear explanations for why certain actions may be necessary during the process.

6. **Redirect command output**: Redirect the output of commands to a file for easier analysis and reference. This will allow you to review the dependencies in a structured format.

7. **Clean up intermediate files**: Remove all intermediate generated files except for the final report.

8. **Do not modify make files**: Avoid making any changes to the make files or build scripts unless explicitly instructed by the user. Always seek permission before making any modifications to the build environment, and provide clear explanations for why certain actions may be necessary during the process. This will help ensure that the user maintains control over their build environment and can make informed decisions about any changes that may be required during the compilation process.

9. **Do not modify source code**: Avoid making any changes to the source code unless explicitly instructed by the user. Always seek permission before making any modifications to the source code, and provide clear explanations for why certain actions may be necessary during the process. This will help ensure that the user maintains control over their codebase and can make informed decisions about any changes that may be required during the compilation process.

10. **Do not modify build environment**: Avoid making any changes to the build environment unless explicitly instructed by the user. Always seek permission before making any modifications to the build environment, and provide clear explanations for why certain actions may be necessary during the process. This will help ensure that the user maintains control over their build environment and can make informed decisions about any changes that may be required during the compilation process.

11. **Do not modify build commands**: Avoid making any changes to the build commands or scripts unless explicitly instructed by the user. Always seek permission before making any modifications to the build commands, and provide clear explanations for why certain actions may be necessary during the process. This will help ensure that the user maintains control over their build process and can make informed decisions about any changes that may be required during the compilation process. 

12. **Do not modify build dependencies**: Avoid making any changes to the build dependencies or library versions unless explicitly instructed by the user. Always seek permission before making any modifications to the build dependencies, and provide clear explanations for why certain actions may be necessary during the process. This will help ensure that the user maintains control over their build environment and can make informed decisions about any changes that may be required during the compilation process.

13. **Do not add any new compiler flags to makefiles**: Avoid adding any new compiler flags or options to the makefiles unless explicitly instructed by the user. Always seek permission before making any modifications to the compiler flags, and provide clear explanations for why certain actions may be necessary during the process. This will help ensure that the user maintains control over their build environment and can make informed decisions about any changes that may be required during the compilation process.

14. **Do not delete any existing files**: Avoid deleting any files from the source code or build environment unless explicitly instructed by the user. Always seek permission before making any modifications to the file structure, and provide clear explanations for why certain actions may be necessary during the process. This will help ensure that the user maintains control over their codebase and can make informed decisions about any changes that may be required during the compilation process.

15. **Learn from mistakes**: If you make a mistake or encounter an error during the process, take help from the user to understand what went wrong and how to fix it. Use this information to improve your understanding of the TMOS compilation process and avoid making similar mistakes in the future. This will help you become more proficient in assisting with TMOS compilation and provide better support to users in the future.

16. **Document your actions**: Keep a record of the commands you run, the changes you make, and the decisions you take during the compilation process. This will help you track your progress and provide a reference for future troubleshooting or optimization efforts. Additionally, it can help other team members understand the steps taken during the compilation process and facilitate collaboration.

17. **Auto update skill or agent or instructions or prompts**: If you find any outdated information in the skill or agent or instructions or prompts, please update it with the latest information. This will help ensure that the user receives accurate and relevant information throughout the compilation process. Always seek permission before making any modifications to the skill or agent or instructions or prompts, and provide clear explanations for why certain updates may be necessary during the process. This will help ensure that the user maintains control over their learning experience and can make informed decisions about any changes that may be required during the compilation process. Also update the relevant files based on the new learnings encountered during any of the context.

18. **Follow best coding practices**: When providing code snippets or examples, ensure that they follow coding best practices and are well-structured, readable, and maintainable. This will help users understand the code more easily and encourage them to adopt good coding habits in their own projects.

19. **Encourage user feedback**: Actively encourage users to provide feedback on the instructions, code snippets, and overall guidance provided. This will help you identify areas for improvement and ensure that the information you provide is relevant and helpful to users. Additionally, it can foster a collaborative learning environment where users feel comfortable sharing their thoughts and suggestions for enhancing the compilation process.

20. **Follow coding guidelines**: Adhere to any specific coding guidelines or standards that are relevant to the TMOS compilation process. This may include following naming conventions, code formatting rules, and other best practices that are commonly accepted in the industry. By following these guidelines, you can help ensure that the code you provide is consistent with industry standards and is easier for users to understand and work with. Use the skill file "coding-guidelines.skill.md" located in the relative path ai-agents/common/skills for reference to the coding guidelines to be followed. 

21. **File location reference**:
  - global common skill files are located in the path relative to the workspace root folder: `ai-agents/common/skills/`
  - global common instructions files are located in the path relative to the workspace root folder: `ai-agents/common/instructions/`
  - Find the <project_name> to be used for the project specific skill files and instructions files from the agent path itself. E.g., if the agent path is `ai-agents/projects/centos2rocky/agents/tmos_rocky_migrator.agent.md`, then the project name is `centos2rocky`. Use this project name to refer to the project specific skill files and instructions files for that project.
  - project specific skill files are located in the path relative to the workspace root folder: `ai-agents/projects/<project_name>/skills/`
  - project specific instructions files are located in the path relative to the workspace root folder: `ai-agents/projects/<project_name>/instructions/`
  - project specific logs are located in the path relative to the workspace root folder: `ai-agents/projects/<project_name>/logs/`
  - project specific output are located in the path relative to the workspace root folder: `ai-agents/projects/<project_name>/output/`
  - project specific input are located in the path relative to the workspace root folder: `ai-agents/projects/<project_name>/input/`
  - project common skill files are located in the path relative to the workspace root folder: `ai-agents/projects/common/skills/`
  - project common instructions files are located in the path relative to the workspace root folder: `ai-agents/projects/common/instructions/`
  - project common agents are located in the path relative to the workspace root folder: `ai-agents/projects/common/agents/`
  - project common sub-agents are located in the path relative to the workspace root folder: `ai-agents/projects/common/sub-agents/`
  - project common input files are located in the path relative to the workspace root folder: `ai-agents/projects/common/input/`

22. **logging**: Log all the steps and actions taken during the process in a structured format. This will help you keep track of the progress and provide a reference for future troubleshooting or optimization efforts. Additionally, it can help other team members understand the steps taken during the compilation process and facilitate collaboration. Store the logs in a single or multiple files in the path relative to the workspace root folder: `ai-agents/projects/<project_name>/logs/`. Ensure that the logs are well-organized and easily accessible for future reference.

24. **Report generation**: After completing the compilation process, generate a comprehensive report that summarizes the steps taken, the changes made, the issues encountered, and the overall outcome of the process. This report should be well-structured and provide insights into the compilation process, summary report on the code changes done to fix the compilation errors, reasons for the compilation errors, general comment about the coding practices followed in the code, etc., including any lessons learned or recommendations for future improvements. Store this report in the path relative to the workspace root folder: `ai-agents/projects/<project_name>/output/`. This will help in documenting the process and providing a reference for future projects or team members who may be working on similar tasks.

25. **existing workspace default path**: In case of existing workspace, if the user had not provided the full path for the existing workspace, check for the existing workspaces in the default path `/local/$USER/sources` or `/local/$USER/` or `/home/$USER/`. Validate if the workspace exists or not. If not, inform the user about the invalid path and prompt them to provide a valid workspace or path. Validate if there is only one existing workspace or multiple workspaces. If there is only one existing workspace, assume that is the workspace user is referring to and proceed with that. If there are multiple workspaces, inform the user about the multiple workspaces and prompt them to provide the full path for the workspace they want to use.

26. **File editing**: Use 'p4 edit` command to grant write permission for the file before editing any file in the source code. This also helps to keep track on the files modified. When editing files, make sure to follow the coding guidelines and best practices to maintain the quality and consistency of the codebase. Additionally, keep track of all the changes made to the files and document them in the logs for future reference.