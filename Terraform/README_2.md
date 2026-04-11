# Terraform state — why it matters

## What is the Terraform state file?

The Terraform state file (`terraform.tfstate`) is a JSON document that acts as the single source of truth for infrastructure managed by Terraform. It maps resources defined in your configuration to real cloud resources, stores metadata and dependencies, and enables reliable planning, updates, and drift detection.

## Key purposes

1. Maps configuration to real infrastructure

   Example Terraform resource:

   ```hcl
   resource "aws_instance" "web" {
     instance_type = "t2.micro"
   }
   ```

   After `terraform apply`, the state stores runtime information (IDs, IPs, etc.):

   ```json
   {
     "aws_instance.web": {
       "id": "i-1234567890",
       "public_ip": "54.23.12.1"
     }
   }
   ```

   This prevents Terraform from creating duplicate resources on subsequent runs.

2. Helps Terraform plan changes

   When you change `instance_type` from `t2.micro` to `t2.small`, Terraform compares the desired config with the state and outputs an accurate plan (e.g., `~ update in-place`). Without state, Terraform cannot determine what already exists.

3. Detects drift

   If someone modifies resources outside Terraform (console or API), `terraform plan` will compare real cloud state to the recorded state and show unexpected changes (drift).

4. Contains sensitive data — treat with care

   The state can include IPs, resource IDs, and sometimes secrets (e.g., DB passwords). Never commit `terraform.tfstate` to version control.

   Example sensitive snippet:

   ```json
   {
     "db_password": "mypassword123"
   }
   ```

   Best practice: store state in a secure remote backend and restrict access.

5. Don't edit state manually

   Manually changing `terraform.tfstate` leads to inconsistencies between the file and real infrastructure and causes unpredictable behavior. Use Terraform commands instead:

   - `terraform state mv`
   - `terraform state rm`
   - `terraform import`

6. Remote state for teams

   Use a shared backend (S3, Terraform Cloud, etc.) so your team uses a single authoritative state.

   Example S3 backend configuration:

   ```hcl
   terraform {
     backend "s3" {
       bucket = "my-terraform-state"
       key    = "prod/terraform.tfstate"
       region = "us-east-1"
     }
   }
   ```

7. State locking to avoid conflicts

   Concurrent `terraform apply` operations can corrupt state. Enable locking (e.g., DynamoDB with S3 backend) so only one worker modifies state at a time.

8. Back up state before major changes

   Keep a backup copy before big changes:

   ```bash
   cp terraform.tfstate terraform.tfstate.backup
   ```

   Backups allow you to restore state if something goes wrong.

## Best practices (summary)

- Store state remotely for teams and secure access control.
- Enable state locking to prevent concurrent writes.
- Never commit state to source control.
- Use Terraform state subcommands or `terraform import` instead of editing the file.
- Keep periodic backups for quick recovery.

---

If you'd like, I can also add a short Table of Contents or convert this into a one-page cheat sheet.