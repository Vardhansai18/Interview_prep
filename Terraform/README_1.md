# 🏗️ Terraform — Interview Questions & Answers

---

## 1. What is Terraform's primary purpose?

Its primary purpose in DevOps is to **automate the infrastructure lifecycle**, enabling teams to build, change, and version infrastructure safely and efficiently. It acts as a single tool to manage infrastructure across multiple cloud providers and on-premises data centers, fostering a consistent workflow.

> 💡 Think of Terraform like a **construction blueprint + automation system** for infrastructure.

---

### � Real-life Example: Building Houses

Imagine a real estate company that needs to build houses in different cities.

#### ❌ Without Terraform (Manual way)

Every time they build a house:
- Hire workers
- Explain the design again
- Buy materials manually
- Hope everything is consistent

**Result:**
- ⚠️ Mistakes happen
- ⚠️ Houses look different
- ⚠️ Takes a lot of time

#### ✅ With Terraform (Automated way)

They create a **standard blueprint** (like Terraform config files).

This blueprint says:
- 2 bedrooms
- 1 kitchen
# 🏗️ Terraform — Interview Questions & Answers

---

## Overview

This note contains concise Terraform interview questions and clear examples you can use during preparation. It covers Terraform's purpose, a real-world analogy, a concrete example, and the difference between declarative and imperative Infrastructure as Code (IaC).

---

## Table of contents

- [What is Terraform?](#what-is-terraform)
- [Real-world analogy](#real-world-analogy)
- [Concrete example](#concrete-example)
- [Declarative vs Imperative IaC](#declarative-vs-imperative-iac)

---

## What is Terraform?

Terraform's primary purpose is to **automate the infrastructure lifecycle**. It lets teams define desired infrastructure in code, then creates, updates, and destroys resources across providers in a consistent, repeatable way.

Key points:

- Single source of truth for infra state
- Works across cloud providers and on-prem
- Enables versioning and review of infra changes

> Tip: Think of Terraform as a blueprint + automation system for infrastructure.

---

## Real-world analogy

Imagine a construction company that builds houses.

### Without Terraform (manual)

- Repeated instructions each time
- More mistakes and inconsistent results
- Time-consuming

### With Terraform (automated)

- One reusable blueprint (.tf files)
- Reproducible results across environments
- Faster and less error-prone

---

## Mapping to DevOps

| Real life              | Terraform equivalent                        |
|------------------------|---------------------------------------------|
| House blueprint        | `.tf` configuration files                   |
| Construction workers   | Cloud providers (AWS, Azure, GCP)           |
| Building a house       | Creating VMs, DBs, networks                 |
| Reusing the blueprint  | Reusable infra code                         |

---

## Concrete example

Suppose you need 2 servers, 1 database, and 1 load balancer. With Terraform you declare resources in one place and run `terraform apply` to provision them.

Example (simplified HCL):

```hcl
resource "aws_instance" "app" {
  ami           = "ami-123456"
  instance_type = "t2.micro"
}

resource "aws_db_instance" "db" {
  engine         = "mysql"
  instance_class = "db.t3.micro"
}
```

Run:

```bash
terraform init
terraform apply
```

---

## 2. Explain the difference between declarative and imperative IaC.


- You declare the desired end state (the "what").
- The tool figures out the "how" (ordering, dependencies, diffs).
- Idempotent and state-aware.

Example (Terraform):

```hcl
resource "aws_instance" "web" {
  ami           = "ami-123456"
  instance_type = "t2.micro"
}
```

What happens: Terraform compares desired vs actual state, then creates/updates/deletes resources to match.

Key traits:

- Idempotent
- State-aware
- Easier to maintain at scale

### Imperative (scripts, step-by-step)

- You write explicit commands to run in order (the "how").
- You must manage ordering, retries, and idempotency yourself.

Example (bash):

```bash
#!/bin/bash
aws ec2 run-instances --image-id ami-123456 --count 1
```

Issues: duplicates if run twice, manual error handling required.

---

## Short analogy

- Declarative → "I want a pizza" (restaurant handles the process)
- Imperative → "Take dough → add sauce → bake at 200°C" (you do every step)

---

If you want, I can:

- shorten this into a single-slide summary
- add more Q&A pairs for interview practice
- commit and push the cleaned `README.md` for you




3.  How does Terraform differ from configuration management tools like Ansible?
Terraform is primarily a provisioning tool, focused on creating, managing, and destroying infrastructure resources like virtual machines, networks, and databases. It excels at managing the lifecycle of these foundational components. Ansible, on the other hand, is primarily a configuration management tool, focused on installing and managing software on existing servers.


4. Explain the basic structure of a Terraform configuration file.
HCL (HashiCorp Configuration Language) is employed to structure a Terraform configuration file. It is made up of parts like variable for input variables, resource to define resources, provider to determine the cloud provider, and output to extract and display values. Parameters and values defining infrastructure settings and components are provided in each block.


5.  What makes Terraform a cloud-agnostic tool?
Terraform is cloud-agnostic due to its provider-based architecture. It uses plugins called "providers" that act as a translation layer between Terraform's universal configuration language and the specific API of a cloud provider (like AWS, Azure, GCP) or other services. This allows a single Terraform configuration and workflow to manage resources across multiple platforms simultaneously. This contrasts with cloud-specific tools like AWS CloudFormation, which only work within their native ecosystem.

6. What is Infrastructure as Code (IaC) and its main benefits?
Infrastructure as Code (IaC) is the practice of managing and provisioning infrastructure through machine-readable configuration files rather than manual processes or interactive tools. Its primary benefits include increased deployment speed and efficiency through automation, enhanced consistency across environments (dev, staging, production), and improved scalability. By versioning infrastructure configurations, teams can track changes, collaborate more effectively, and significantly reduce the risk of human error.

7. Describe the core Terraform workflow.
The core Terraform workflow consists of three main steps: Write, Plan, and Apply. First, you Write infrastructure as code in HCL files. Next, you run terraform plan to generate an execution Plan, which previews the changes Terraform will make to your infrastructure without actually applying them. Finally, you use terraform apply to Apply the changes and provision or modify the resources as described in the plan. This cycle provides a safe and predictable way to manage infrastructure.

8. What is the purpose of terraform init?
The terraform init command is used to initialize a working directory containing Terraform configuration files. It performs three primary tasks: it downloads and installs the provider plugins declared in the configuration, initializes the configured backend for state file storage, and downloads any modules referenced in the configuration. This command must be run before any other Terraform commands can be executed in a new or cloned project directory.


9. Explain what terraform plan does and why it's important.
The terraform plan command creates an execution plan by comparing the desired state defined in your configuration files against the current state of the real-world infrastructure recorded in the state file. The output shows exactly which resources will be created, updated, or destroyed. This command is critically important because it provides a "dry run" or preview of changes, allowing for review and validation before any modifications are made to the actual infrastructure, thereby preventing unintended or destructive actions.



10. . What is the difference between terraform apply and terraform apply tfplan?
Running terraform apply without an argument will first generate a new execution plan and then prompt for interactive approval before executing it. This is suitable for manual workflows. In contrast, terraform apply tfplan, where tfplan is a file saved from a terraform plan -out=tfplan command, applies the exact changes outlined in that pre-saved plan file without generating a new one or prompting for approval. The latter is a best practice for automation and CI/CD pipelines, as it ensures that only the previously reviewed and approved changes are executed.

