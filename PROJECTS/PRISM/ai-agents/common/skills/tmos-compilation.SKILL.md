---
skill: tmos-compilation
description: Domain knowledge for TMOS (Traffic Management Operating System) compilation, build processes, and 64-bit migration. USE FOR tasks involving TMOS module building, dependency management, 32-bit to 64-bit migration, and Rocky Linux compilation. Provides build commands, compilation best practices, and migration guidelines.
applyTo:
  - "**/*"
---

# TMOS Compilation Skill

## BUILD COMMANDS REFERENCE

### Workspace Management

**Create new workspace:**
```bash
cd /local/$USER/sources
~/create_ws <branch-name>
```

**Setup build environment:**
```bash
./build -setup latest
./build -prebuilt
```

### Module Information

**List all available packages/modules:**
```bash
./build -print_pkgs <module-name>
```
The above command will return below output if the module name is valid:
```Output package list for (<module_name>):```
on the other hand, if the module name is invalid, it will return an error message like below:
``` <module_name>: not a valid entry name. Operation aborted. ```

Note: Check for the exact module name as there could be modules with similar names with different suffix or prefix (e.g., mcplib, mcplib_common, tamdlib, tamd).

**Print module dependencies:**
```bash
./build -print_depends 50 <module-name>
```

### Compilation Commands

**Compile module with dependency check:**
```bash
./build <module-name> -j 64
```

**Compile module without dependency check:**
```bash
./build -nodep <module-name> -j 64
```

**Clean module with dependent modules:**
```bash
./build -clean <module-name> -j 64
```

**Clean module without dependent modules:**
```bash
./build -nodep -clean <module-name> -j 64
```

### Source Code Management

**Checkout code for a module:**
```bash
./build -p4 <module-name>
```

**Open file for editing (Perforce):**
```bash
p4 edit <file-path>
```

## WORKSPACE SETUP PROCESS

1. **Check workspace preference**: Ask the user if they want to use a new workspace or an existing workspace for the compilation.

2. **For new workspace:**
   - Ask the user to input the branch name
   - Create new workspace using the commands above
   - Inform the user that the new workspace has been created successfully
   - Switch to the new workspace

3. **For existing workspace:**
   - Ask them to provide the path to their existing workspace
   - Verify that it is valid before proceeding

4. **Build environment setup:**
   - Ask the user if they have already set up their build environment
   - If not, ask permission to setup the build environment
   - If they agree, inform them that setting up will take some time
   - Run the setup commands (`.'/build -setup latest` and `./build -prebuilt`)
   - If already set up, ask if they would like to update to the latest version

5. **Error checking**: Check for errors during the setup process and inform the user if there are any issues that need to be resolved before proceeding with the compilation.

## 64-BIT MIGRATION GUIDELINES

### Module Definition Structure

Look for module definitions in `*.inc` files in the workspace. Module definitions follow this template:

```
<module-name>: {
    context:        arch=x86_64
    perforce:       <module source code path in perforce>
    prompt:         <Description of the module>
    ...
}
```

### Pre-Migration Checklist

Before starting migration:
1. Validate the module name using `./build -print_pkgs`
2. Identify all dependencies using `./build -print_depends 50 <module-name>`
3. Ensure dependent modules are already migrated to 64-bit architecture
4. Checkout the source code using `./build -p4 <module-name>`
5. Get explicit user confirmation before making any changes

### Common Migration Considerations

- Update data types to be 64-bit compatible
- Review pointer arithmetic and casting
- Check memory management practices
- Update architecture context in module definitions
- Verify library dependencies are 64-bit compatible
- Test compilation after changes

## BEST PRACTICES

1. **Always redirect output**: Save command outputs to files for analysis
2. **Incremental approach**: Make changes incrementally and test frequently
3. **Dependency awareness**: Always check and migrate dependencies first
4. **Version control**: Use Perforce commands to track all changes
5. **Error handling**: Address compilation errors systematically
6. **Documentation**: Keep notes on changes made during migration
7. **Cleanup**: Remove intermediate files when done

## TROUBLESHOOTING

- If `./build -print_pkgs` doesn't show your module, verify the module name spelling
- If compilation fails with dependency errors, check if all dependent modules are built
- If permission denied errors occur, ensure files are checked out with `p4 edit`
- If environment setup fails, check disk space and network connectivity

## ROCKY LINUX SPECIFIC NOTES

When migrating to Rocky Linux:
- Ensure compiler versions are compatible
- Check for distribution-specific library paths
- Verify system dependencies are installed
- Test build on Rocky Linux environment before finalizing

---

**Note**: This skill is automatically applied when working with TMOS-related files. For specific migration workflows, refer to the tmos_64bit_migrator or tmos_rocky_migrator agents.
