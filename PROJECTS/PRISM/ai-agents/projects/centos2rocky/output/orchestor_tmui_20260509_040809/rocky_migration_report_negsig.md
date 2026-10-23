# Rocky Linux 8.10 Migration Report: negsig

## Summary
- **Module**: negsig
- **Dependency Level**: level-15
- **Migration Status**: Completed
- **Build**: Successful (Build #13)

## Changes Made

### TrafficShield/negsig/Makefile
- Added `LD_LIBRARY_PATH` with `devfs_x86_64` path for YAML::XS LibYAML shared library
- Added `-I$(DEVFS)_x86_64/usr/lib64/perl5/vendor_perl` to `generate_attack_types` Perl include path
- Added devfs_x86_64 paths for `generate_sigfile_schema` target (F5::XML::Twig)
- Root cause: negsig is a noarch package (devfsdir=devfs) but YAML::XS is only available in devfs_x86_64

### TrafficShield/negsig/negsig.new.spec
- Added `%undefine _debugsource_packages`
- Added `%include %{_topdir}/gcc-toolchain.inc`
- Added `%{gcc_toolset_enable}` in `%build` section
- Updated `make` invocation to include `DEVFS=%{devfsdir}`

### TrafficShield/common/* Makefiles
- Rocky Linux 8.10 GCC toolset compatibility updates

### TrafficShield/xml/processor/
- Rocky Linux 8.10 build compatibility fixes

## Build Results
- **RPM**: TS-negsig-22.0.0-0.0.162.noarch.rpm
- **Build Log**: ai-agents/projects/centos2rocky/logs/negsig/tmos_rocky_migrator_negsig_build13.log

## Testing
- RPM built successfully on Rocky Linux 8.10
