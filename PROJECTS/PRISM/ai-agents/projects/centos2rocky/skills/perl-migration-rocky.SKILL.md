---
name: perl-migration-rocky
description: Domain knowledge for migrating Perl applications to the version supported by Rocky Linux 8.10. Covers Perl 5.26+ compatibility, deprecated features, module updates, and best practices for enterprise Linux migration. Also applies to extensionless scripts with perl shebang lines (e.g., tm_lib/mcp/construct).
applyTo: ["**/*.pl", "**/*.pm", "**/*.t", "**/Makefile.PL", "**/Build.PL", "**/cpanfile", "**/*.spec", "**/construct", "**/bin/*"]
---

# Perl Migration Guide: Legacy Perl → Rocky Linux 8.10 (Perl 5.26+)

This skill provides comprehensive guidance for migrating Perl applications to Rocky Linux 8.10, which provides Perl 5.26.3 as the default version, with Perl 5.30 and 5.32 available via Application Streams.

## Important Note on Package Management

**This guide identifies required packages but does not install them automatically.**

When migrating Perl applications, this skill will:
- Identify all required Perl modules and packages
- Document package names and dependencies
- Provide installation commands for user reference
- Recommend appropriate package sources (DNF repositories vs. CPAN)

**All package installations require explicit user action.** The agent will inform you about:
- Required system packages (perl-*, development tools)
- Missing CPAN modules
- Optional packages for enhanced functionality
- Dependencies and prerequisites

Users should review all package requirements and install them according to their organization's policies and procedures.

## Rocky Linux 8.10 Perl Environment

### Available Perl Versions

**Default Perl:**
- **Perl 5.26.3** - Default system Perl in Rocky Linux 8.10
- Installed at: `/usr/bin/perl`
- Package: `perl` (base system)

**Module Streams (AppStream):**
- **Perl 5.30** - Available via module stream `perl:5.30`
- **Perl 5.32** - Available via module stream `perl:5.32`

**To enable a specific version, user needs to:**
```bash
# Check available streams
dnf module list perl

# Enable Perl 5.32 stream (requires user action)
dnf module enable perl:5.32

# Install Perl 5.32 (requires user action)
dnf install perl
```

**Note:** Inform the user if a specific Perl version is required for their application.

### Key Changes from Older Perl Versions

This guide covers migration from Perl 5.8, 5.10, 5.14, 5.16, 5.18, 5.20, and 5.24 to Perl 5.26+.

## Critical Breaking Changes

### 1. Removal of Current Directory (.) from @INC

**MOST IMPORTANT CHANGE in Perl 5.26+**

**Old Behavior (Perl 5.24 and earlier):**
```perl
# Current directory was in @INC
# This worked:
require "mylib.pl";        # Loaded from ./mylib.pl
do "config.pl";            # Loaded from ./config.pl
use MyModule;              # Could load ./MyModule.pm

# Scripts could load modules from current directory
./myscript.pl              # Could find modules in same directory
```

**New Behavior (Perl 5.26+):**
```perl
# Current directory (.) removed from @INC for security
# These will fail unless module is in standard @INC path:
require "mylib.pl";        # ERROR: Can't locate mylib.pl in @INC
do "config.pl";            # ERROR: Can't locate config.pl in @INC
use MyModule;              # ERROR: Can't locate MyModule.pm in @INC
```

**Solutions:**

**Solution 1: Use explicit paths**
```perl
# Use explicit relative or absolute paths
require "./mylib.pl";           # Explicit current directory
do "/path/to/config.pl";        # Absolute path

# For modules in current directory
use lib '.';                    # Add current dir to @INC
use MyModule;

# Or use FindBin
use FindBin qw($Bin);
use lib $Bin;                   # Add script's directory to @INC
use MyModule;
```

**Solution 2: Install modules properly**
```perl
# Install modules to standard location
# In your project structure:
# lib/MyModule.pm
use lib 'lib';
use MyModule;

# Or use FindBin for portability
use FindBin qw($Bin);
use lib "$Bin/../lib";
use MyModule;
```

**Solution 3: Use -I flag**
```bash
# Add directory to @INC via command line
perl -I. myscript.pl
perl -I/path/to/lib myscript.pl

# In shebang
#!/usr/bin/perl -I.
#!/usr/bin/perl -I/opt/myapp/lib
```

**Solution 4: Set PERL5LIB environment variable**
```bash
export PERL5LIB=/path/to/lib:.
perl myscript.pl
```

### 2. Lexical Subroutines (my sub) No Longer Experimental

**Perl 5.26+:**
```perl
# Lexical subroutines are now stable
my sub helper {
    my ($arg) = @_;
    return $arg * 2;
}

# No longer need experimental pragma
# use experimental 'lexical_subs';  # Not needed in 5.26+
```

### 3. Unicode Improvements and Changes

**Perl 5.26+:**
```perl
# Better Unicode handling
# Unicode 9.0 support in Perl 5.26
# Unicode 13.0 support in Perl 5.32

# Use utf8 for source code
use utf8;

# Enable Unicode output
binmode(STDOUT, ":utf8");
binmode(STDERR, ":utf8");

# Open files with encoding
open my $fh, '<:encoding(UTF-8)', $filename;
```

### 4. Deprecated Features Removed

**Removed in Perl 5.26+:**

```perl
# 1. ${^ENCODING} removed
# OLD - Don't use
${^ENCODING} = "utf-8";  # REMOVED

# NEW - Use proper encoding layers
open my $fh, '<:encoding(UTF-8)', $file;

# 2. Bareword file handles (discouraged)
# OLD - Avoid
open FILE, "<", $filename;
print FILE "data";
close FILE;

# NEW - Use lexical file handles
open my $fh, "<", $filename or die "Cannot open: $!";
print $fh "data";
close $fh;

# 3. Unescaped literal "{" and "}" in regex (warnings/errors)
# OLD - Warning in 5.26+, error in future versions
/foo{/;        # Warning: Unescaped left brace

# NEW - Escape braces
/foo\{/;       # Correct
/foo[{]/;      # Or use character class
```

### 5. Hash Randomization (Security Enhancement)

**Perl 5.18+:**
```perl
# Hash key order is randomized for security
# Don't rely on hash order
my %hash = (a => 1, b => 2, c => 3);
foreach my $key (keys %hash) {
    # Order is NOT guaranteed
}

# If order matters, use sort
foreach my $key (sort keys %hash) {
    # Alphabetical order
}

# Or use ordered hash module
use Tie::IxHash;
tie my %ordered_hash, 'Tie::IxHash';
$ordered_hash{a} = 1;
$ordered_hash{b} = 2;
```

### 6. 64-bit Integers

**Rocky Linux 8 (64-bit):**
```perl
# Perl compiled with 64-bit integer support
use Config;
print "Integer size: ", $Config{ivsize}, " bytes\n";  # Usually 8

# Large integers work natively
my $big = 9223372036854775807;  # max 64-bit signed int

# Be aware of portability issues
# Code migrated from 32-bit systems may behave differently
```

## Common Deprecated Features

### 1. defined(@array) and defined(%hash)

**Old (Deprecated):**
```perl
# Don't check if array/hash is defined
if (defined @array) {    # DEPRECATED
    # ...
}
if (defined %hash) {     # DEPRECATED
    # ...
}
```

**New:**
```perl
# Check if array/hash has elements
if (@array) {            # True if array has elements
    # ...
}
if (%hash) {             # True if hash has key-value pairs
    # ...
}

# Or check explicitly
if (scalar @array > 0) {
    # ...
}
if (scalar keys %hash > 0) {
    # ...
}
```

### 2. Bareword File Handles

**Old:**
```perl
# Global bareword file handles
open FILE, "<", $filename or die $!;
while (<FILE>) {
    print;
}
close FILE;

# Two-argument open (deprecated)
open FILE, "< $filename";     # Insecure
open FILE, "| command";       # Insecure
```

**New:**
```perl
# Lexical file handles (preferred)
open my $fh, "<", $filename or die "Cannot open $filename: $!";
while (<$fh>) {
    print;
}
close $fh;

# Three-argument open (secure)
open my $fh, "<", $filename or die $!;
open my $pipe, "-|", "command", @args or die $!;
```

### 3. Indirect Object Syntax

**Old:**
```perl
# Indirect object syntax (ambiguous)
my $obj = new MyClass;           # Can be parsed incorrectly
my $fh = new IO::File $filename; # Ambiguous

# Error prone
my $result = some_func MyClass;  # Is MyClass a package or variable?
```

**New:**
```perl
# Direct method call (preferred)
my $obj = MyClass->new();
my $fh = IO::File->new($filename);

# Clear and unambiguous
my $result = some_func('MyClass');
```

### 4. Autovivification in Conditionals

**Old Behavior:**
```perl
# Creates hash entries even when just checking
my %hash;
if ($hash{key}{subkey}) {   # Autovivifies $hash{key}
    # ...
}
# Now exists($hash{key}) is true even if never set
```

**Better Practice:**
```perl
# Use exists() to check without autovivifying
my %hash;
if (exists $hash{key} && exists $hash{key}{subkey}) {
    # ...
}

# Or use autovivification pragma
use autovivification 'warn';  # Warn on autovivification
# or
no autovivification;          # Disable autovivification
```

### 5. qw() Comma Behavior

**Perl 5.26+:**
```perl
# Literal commas in qw() now produce warnings
my @list = qw(a b,c d);  # Warning: comma in qw() list

# Separate properly
my @list = qw(a b c d);  # Correct
```

## Module and CPAN Changes

### 1. Core Module Removals

**Modules removed from core (need separate installation):**

```perl
# These are no longer in core Perl 5.26+
use CGI;                 # Requires: perl-CGI package (dnf install perl-CGI)
use Module::Build;       # Requires: perl-Module-Build package
use Switch;              # Removed, use given/when or if/elsif

# Check if module is core
perl -MModule::CoreList -e 'print Module::CoreList->first_release("CGI")'
```

**Note:** If these modules are used in the code, inform the user that the following packages need to be installed:
- `perl-CGI` for CGI module
- `perl-Module-Build` for Module::Build

### 2. Required CPAN Modules for Rocky Linux

**Inform user about required packages from DNF repositories (preferred):**
```bash
# User can search for Perl modules with:
dnf search perl-Module-Name

# Common required packages that user may need to install:
# - perl-DBI (database interface)
# - perl-DBD-MySQL (MySQL driver)
# - perl-JSON (JSON support)
# - perl-LWP-Protocol-https (HTTPS support)
# - perl-DateTime (date/time handling)

# Development tools the user may need:
# - perl-devel (Perl development files)
# - perl-CPAN (CPAN client)
# - "Development Tools" group (compilers, make, etc.)
```

**If user needs to install from CPAN:**
```bash
# User can configure CPAN (first time)
cpan

# User can install modules with:
cpan Module::Name
cpan DBI
cpan Mojolicious

# Or using cpanm (requires perl-App-cpanminus package):
cpanm Module::Name
cpanm --local-lib=~/perl5 Module::Name  # Local installation
```

**For non-root installation (requires perl-local-lib package):**
```bash
# User needs perl-local-lib package installed

# User can set up local::lib environment:
echo 'eval "$(perl -I$HOME/perl5/lib/perl5 -Mlocal::lib)"' >> ~/.bashrc
source ~/.bashrc

# Then install modules locally with cpanm
```

**Note:** Always inform the user about required packages rather than installing them automatically.

### 3. Module Version Compatibility

**Check module compatibility:**
```perl
#!/usr/bin/perl
use strict;
use warnings;

# Check module version
use Module::Name;
print "Version: ", $Module::Name::VERSION, "\n";

# Check Perl version requirements
use 5.026;  # Require Perl 5.26 or higher
```

**Note:** If the application requires specific module versions, document them and inform the user about version requirements before they install packages.

## Migration Patterns

### Pattern 1: Fixing @INC Issues

**Before:**
```perl
#!/usr/bin/perl
use strict;
use warnings;

# Assumes current directory in @INC
require "config.pl";
use MyLocalModule;

# Load data file
do "data.pl";
```

**After:**
```perl
#!/usr/bin/perl
use strict;
use warnings;
use FindBin qw($Bin);
use lib $Bin;              # Add script directory to @INC

# Explicit path for requires
require "$Bin/config.pl";
use MyLocalModule;         # Now can find in script directory

# Load data file with explicit path
do "$Bin/data.pl";
```

### Pattern 2: Modernizing File Handles

**Before:**
```perl
# Old style with barewords
open FILE, "< $filename" or die $!;
while (<FILE>) {
    chomp;
    print FILE2 $_;
}
close FILE;
close FILE2;
```

**After:**
```perl
# Modern style with lexical file handles
open my $in_fh, "<", $filename or die "Cannot open $filename: $!";
open my $out_fh, ">", $outfile or die "Cannot open $outfile: $!";

while (my $line = <$in_fh>) {
    chomp $line;
    print {$out_fh} $line;
}

close $in_fh or warn "Cannot close input: $!";
close $out_fh or warn "Cannot close output: $!";
```

### Pattern 3: Hash Iteration (Order Independence)

**Before:**
```perl
# Code that assumes hash order
my %config = (
    host => 'localhost',
    port => 3306,
    db   => 'mydb',
);

# This order is NOT guaranteed
foreach my $key (keys %config) {
    print "$key: $config{$key}\n";
}
```

**After:**
```perl
# Use sort for predictable order
my %config = (
    host => 'localhost',
    port => 3306,
    db   => 'mydb',
);

# Sorted alphabetically
foreach my $key (sort keys %config) {
    print "$key: $config{$key}\n";
}

# Or use array of pairs for ordered config
my @config = (
    host => 'localhost',
    port => 3306,
    db   => 'mydb',
);
for (my $i = 0; $i < @config; $i += 2) {
    print "$config[$i]: $config[$i+1]\n";
}
```

### Pattern 4: Unicode File Handling

**Before:**
```perl
# No explicit encoding
open my $fh, "<", $filename;
my $content = <$fh>;
print $content;
close $fh;
```

**After:**
```perl
# Explicit UTF-8 encoding
use open ':std', ':encoding(UTF-8)';  # Set default for STDIN/STDOUT/STDERR

open my $fh, "<:encoding(UTF-8)", $filename or die $!;
my $content = <$fh>;
print $content;  # Already UTF-8 encoded
close $fh;

# Or set per-handle
open my $fh, "<", $filename or die $!;
binmode($fh, ":encoding(UTF-8)");
```

### Pattern 5: Regex Metacharacter Escaping

**Before:**
```perl
# Unescaped braces (warning in 5.26+)
if ($text =~ /pattern{/) {
    print "Found\n";
}

# Multiple issues
if ($text =~ /{some}pattern{/) {
    print "Match\n";
}
```

**After:**
```perl
# Escape literal braces
if ($text =~ /pattern\{/) {
    print "Found\n";
}

# Or use character class
if ($text =~ /pattern[{]/) {
    print "Found\n";
}

# Or use \Q...\E for literal strings
my $literal = "pattern{";
if ($text =~ /\Q$literal\E/) {
    print "Found\n";
}
```

### Pattern 6: Three-Argument Open

**Before:**
```perl
# Two-argument open (insecure)
my $file = "data.txt";
open FILE, "< $file" or die $!;

# Dangerous with user input
my $user_file = get_user_input();
open FILE, "< $user_file";  # Can be exploited: "|dangerous command"
```

**After:**
```perl
# Three-argument open (secure)
my $file = "data.txt";
open my $fh, "<", $file or die "Cannot open $file: $!";

# Safe with user input
my $user_file = get_user_input();
open my $fh, "<", $user_file or die $!;  # Cannot inject shell commands
```

## Subroutine Signatures (Experimental in 5.26, Stable in 5.36)

**Perl 5.26-5.34 (Experimental):**
```perl
use experimental 'signatures';

# Subroutine signatures
sub greet($name, $age = 18) {
    print "Hello, $name! You are $age years old.\n";
}

greet("Alice", 25);
greet("Bob");  # Uses default age
```

**Note:** For production code on Rocky Linux 8.10, avoid experimental features unless necessary. Use traditional argument handling:

```perl
# Traditional parameter handling (stable)
sub greet {
    my ($name, $age) = @_;
    $age //= 18;  # Default value
    print "Hello, $name! You are $age years old.\n";
}
```

## Testing Strategy

### 1. Version Detection

```perl
#!/usr/bin/perl
use strict;
use warnings;

# Check Perl version
print "Perl version: $^V\n";
print "Perl version number: $]\n";

# Require minimum version
use 5.026;  # Die if Perl < 5.26

# Conditional code based on version
use version;
my $perl_version = version->parse($^V);
if ($perl_version >= version->parse('5.26.0')) {
    print "Running Perl 5.26 or higher\n";
}
```

### 2. Test @INC Issues

```bash
# Run with warnings
perl -w myscript.pl

# Check @INC contents
perl -e 'print join("\n", @INC), "\n"'

# Test with current directory explicitly added
perl -I. myscript.pl

# Lint check
perl -c myscript.pl
```

### 3. Module Testing

```perl
# test.t
use Test::More tests => 5;
use strict;
use warnings;

# Test module loads
use_ok('MyModule');

# Test functions
can_ok('MyModule', qw(function1 function2));

# Test behavior
my $result = MyModule::function1();
is($result, 'expected', 'function1 returns correct value');

# Test with different Perl versions
done_testing();
```

### 4. Automated Testing

```bash
# Run test suite
prove -l t/

# With verbose output
prove -lv t/

# Parallel testing
prove -j4 t/

# Test single file
perl t/test.t
```

## Common Pitfalls and Solutions

### Pitfall 1: Current Directory Not in @INC

**Problem:**
```perl
# Fails on Perl 5.26+
require "mylib.pl";  # Can't locate mylib.pl
use MyModule;        # Can't locate MyModule.pm
```

**Solution:**
```perl
# Use explicit paths or add to @INC
use FindBin qw($Bin);
use lib $Bin;
require "$Bin/mylib.pl";
use MyModule;
```

### Pitfall 2: Hash Randomization Breaks Tests

**Problem:**
```perl
# Test assumes specific hash order
my %hash = (a => 1, b => 2, c => 3);
my @keys = keys %hash;
is_deeply(\@keys, ['a', 'b', 'c'], 'keys in order');  # FAILS randomly
```

**Solution:**
```perl
# Sort keys for consistent order
my %hash = (a => 1, b => 2, c => 3);
my @keys = sort keys %hash;
is_deeply(\@keys, ['a', 'b', 'c'], 'keys in alphabetical order');  # PASSES
```

### Pitfall 3: Unescaped Braces in Regex

**Problem:**
```perl
# Warning in 5.26+, error in future versions
if ($text =~ /foo{bar}/) {   # Warning: Unescaped left brace
    print "Match\n";
}
```

**Solution:**
```perl
# Escape braces or use \Q..\E
if ($text =~ /foo\{bar\}/) {
    print "Match\n";
}

# Or for literal matching
if ($text =~ /\Qfoo{bar}\E/) {
    print "Match\n";
}
```

### Pitfall 4: CGI.pm Not Available

**Problem:**
```perl
use CGI;  # Can't locate CGI.pm in @INC
```

**Solution:**
Inform the user that the `perl-CGI` package is required:
```bash
# User needs to install CGI module:
dnf install perl-CGI

# Or recommend modern web frameworks:
# - perl-Mojolicious (Mojolicious framework)
# - perl-Dancer2 (Dancer2 framework)  
# - perl-Catalyst (Catalyst framework)
```

**Note:** Recommend using modern web frameworks instead of CGI.pm for new development.

### Pitfall 5: Binary/Text File Mode on Windows (Less common on Linux)

**Problem:**
```perl
# May have issues with binary files
open my $fh, "<", "binary.dat";
my $data = <$fh>;
```

**Solution:**
```perl
# Use binary mode for binary files
open my $fh, "<:raw", "binary.dat" or die $!;
# or
open my $fh, "<", "binary.dat" or die $!;
binmode($fh);

# Use encoding for text files
open my $fh, "<:encoding(UTF-8)", "text.txt" or die $!;
```

## Rocky Linux Specific Considerations

### 1. System Perl vs. Application Perl

**Best Practices:**
```bash
# Don't modify system Perl
# System packages depend on /usr/bin/perl

# For applications, recommend user to consider:
# 1. Local Perl installation (requires perlbrew)
perlbrew install perl-5.32.0
perlbrew use perl-5.32.0

# 2. Or use module streams (user action required)
dnf module enable perl:5.32
dnf install perl

# 3. Or use containers (no system modification)
podman run -v $(pwd):/app perl:5.32 perl /app/script.pl
```

**Note:** Inform user about these options and let them choose the appropriate approach for their environment.

### 2. SELinux Considerations

```bash
# SELinux may block Perl scripts
# Check SELinux denials
ausearch -m avc -ts recent

# Set proper context for Perl scripts
# For CGI scripts
chcon -t httpd_sys_script_exec_t script.pl

# For system scripts
chcon -t bin_t script.pl

# Or disable SELinux (not recommended for production)
setenforce 0
```

### 3. Package Management

**Inform user about available package management commands:**
```bash
# User can search for Perl modules:
dnf search perl | grep -i module-name

# List currently installed Perl modules:
dnf list installed | grep perl

# Check module dependencies before installation:
dnf repoquery --requires perl-DBI

# Common Perl packages available in Rocky Linux repositories:
# - perl-DBI (database interface)
# - perl-DBD-MySQL (MySQL database driver)
# - perl-DateTime (date/time handling)
# - perl-JSON (JSON parsing)
# - perl-YAML (YAML parsing)
# - perl-LWP-Protocol-https (HTTPS support)
# - perl-XML-LibXML (XML parsing)
# - perl-Test-Simple (testing framework)
```

**Note:** Document all required Perl packages for the application and inform user to install them.

## Migration Checklist

### Phase 1: Assessment
- [ ] Identify Perl version currently in use
- [ ] List all Perl scripts and modules in application
- [ ] Identify CPAN module dependencies
- [ ] Check for deprecated feature usage
- [ ] Review use of current directory (.) in @INC
- [ ] Identify bareword file handles
- [ ] Check for two-argument open() calls

### Phase 2: Code Updates
- [ ] Add `use strict;` and `use warnings;` to all files
- [ ] Fix @INC issues (add explicit paths or use FindBin)
- [ ] Convert bareword file handles to lexical
- [ ] Change two-argument open to three-argument
- [ ] Escape unescaped braces in regular expressions
- [ ] Remove deprecated defined(@array) and defined(%hash)
- [ ] Sort hash keys where order matters
- [ ] Add explicit UTF-8 encoding for file operations

### Phase 3: Module Updates
- [ ] Identify missing core modules (CGI, Module::Build) and inform user about required packages
- [ ] Document CPAN modules that need to be updated to latest compatible versions
- [ ] List all module dependencies for user review
- [ ] Identify deprecated modules and recommend alternatives
- [ ] Create comprehensive list of all external module dependencies with package names

### Phase 4: Testing
- [ ] Run syntax check: `perl -c script.pl`
- [ ] Run with warnings: `perl -w script.pl`
- [ ] Execute test suite: `prove -l t/`
- [ ] Test on Rocky Linux 8.10 test environment
- [ ] Test with different Perl versions (5.26, 5.30, 5.32)
- [ ] Perform integration testing
- [ ] Load/stress testing for production apps

### Phase 5: Deployment
- [ ] Update shebang lines if needed
- [ ] Set up proper @INC paths in production
- [ ] Configure SELinux contexts (inform user about required chcon commands)
- [ ] Provide list of all required RPM packages for user to install
- [ ] Document complete deployment procedure including package installation steps
- [ ] Create rollback plan
- [ ] Monitor logs after deployment

## Useful Tools

### Development Tools

**Required packages for development (inform user):**
```bash
# Development environment packages:
# - "Development Tools" group (gcc, make, etc.)
# - perl-devel (Perl development headers)
# - perl-CPAN (CPAN client)

# Perl utilities (already available in base perl):
perldoc perldiag        # Diagnostic messages
perldoc perldelta       # What's new in this Perl
perldoc -f function     # Function documentation
perldoc Module::Name    # Module documentation

# Code quality tools (inform user about these packages):
# - perl-Perl-Critic (code quality checker)
# - perl-Test-Simple (basic testing)
# - perl-Test-More (advanced testing)

# Usage examples after packages are installed:
perlcritic script.pl    # Requires perl-Perl-Critic
```

**Note:** Provide user with a complete list of development packages needed.

### Debugging
```bash
# Run with debugger
perl -d script.pl

# Print @INC
perl -V
perl -e 'print "$_\n" for @INC'

# Check module installation
perl -MModule::Name -e 'print $Module::Name::VERSION'

# Trace execution
perl -d:Trace script.pl

# Profile code (requires perl-Devel-NYTProf package)
perl -d:NYTProf script.pl
nytprofhtml
```

**Note:** If profiling is needed, inform user to install `perl-Devel-NYTProf` package.

## Performance Considerations

### Perl 5.26+ Performance Improvements

**Hash performance:**
```perl
# Hash operations are faster in 5.26+
# But order is randomized for security
my %hash = map { $_ => $_ * 2 } (1..1000);
```

**Regex improvements:**
```perl
# Faster regex compilation and execution
my $pattern = qr/complex.*pattern\d+/;
$text =~ $pattern;  # Compiled once, faster execution
```

**Memory usage:**
```perl
# Better memory management in 5.26+
# Reduced memory overhead for large data structures
```

## Additional Resources

- Perl 5.26 Release Notes: https://perldoc.perl.org/perl5260delta
- Perl 5.30 Release Notes: https://perldoc.perl.org/perl5300delta
- Perl 5.32 Release Notes: https://perldoc.perl.org/perl5320delta
- Rocky Linux Documentation: https://docs.rockylinux.org/
- CPAN: https://www.cpan.org/
- MetaCPAN: https://metacpan.org/
- Perl Maven: https://perlmaven.com/
- Modern Perl Book: http://modernperlbooks.com/

## Summary

Key migration points for Rocky Linux 8.10 (Perl 5.26+):

1. **@INC Changes**: Current directory (.) removed from @INC - use explicit paths
2. **File Handles**: Use lexical file handles instead of barewords
3. **Three-Argument Open**: Always use three-argument open for security
4. **Hash Randomization**: Don't rely on hash key order
5. **Unicode**: Use explicit UTF-8 encoding for file operations
6. **Package Requirements**: Document all required packages and inform user (prefer DNF packages over CPAN)
7. **Testing**: Comprehensive testing is essential
8. **SELinux**: Configure proper contexts for scripts (inform user about required commands)
9. **Deprecated Features**: Remove deprecated constructs
10. **Modern Practices**: Follow modern Perl best practices

**Package Installation Policy:** This skill identifies and documents all required packages but does not install them automatically. Users must review and install packages according to their organization's procedures.

The migration to Perl 5.26+ on Rocky Linux 8.10 requires careful attention to security improvements (especially @INC changes) and best practices, but provides better performance, security, and maintainability.
