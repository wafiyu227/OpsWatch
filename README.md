# OpsWatch 🛠️

**A progressively evolving system health monitoring and infrastructure automation project built with Python and Cloud/DevOps technologies.**

OpsWatch is a hands-on learning project designed to evolve from a simple Python command-line tool into a cloud-hosted monitoring platform. It brings together software development, Linux system administration, networking, containerization, cloud infrastructure, automation, and observability in one continuous project.

Rather than learning each technology in isolation, OpsWatch provides a practical environment to apply every new concept as it is learned.

> **Project status:** Stage 1 — Python CLI development
> **Current milestone:** Building the command-line interface (CLI) skeleton.

## 📌 Project Objectives

The primary goal of OpsWatch is to build practical Cloud/DevOps engineering skills through incremental development and real-world problem-solving.

The project aims to:

- Develop a Python-based tool for checking service and URL health.
- Monitor basic system information and measure response times.
- Record health-check results for future analysis.
- Learn Linux administration by running and managing the application on a Linux system.
- Apply networking concepts to connectivity diagnostics.
- Containerize the application using Docker.
- Deploy and manage infrastructure on AWS.
- Automate infrastructure provisioning with Terraform.
- Build a CI/CD pipeline using GitHub Actions.
- Implement monitoring and observability with Prometheus and Grafana.
- Explore Kubernetes for container orchestration.

## ✨ Planned Features

### Current Stage: Python CLI

The initial version will provide:

- An interactive command-line menu.
- Service status checks.
- URL reachability checks.
- HTTP response-time measurement.
- Basic system information reporting.
- Health-check logging to a file.
- Error handling and clear user feedback.

Features will be implemented incrementally. Items in this list represent the intended scope of Stage 1 and may not yet be available in the application.

### Future Capabilities

As development progresses, OpsWatch will expand to include:

- DNS resolution and port checks.
- TCP connectivity diagnostics.
- Linux process and service management.
- Automated execution through systemd and Bash.
- Docker containerization and Docker Compose.
- Cloud deployment and infrastructure management.
- Automated testing, builds, and deployments.
- Metrics collection, dashboards, and alerting.
- Kubernetes-based application deployment.

## 🧰 Technology Roadmap

| Stage | Technology             | Purpose                                                      |
| ----- | ---------------------- | ------------------------------------------------------------ |
| 1     | Python                 | Build the CLI and health-check functionality                 |
| 2     | Linux, Bash, systemd   | Operate and automate the application on Linux                |
| 3     | Networking             | Implement DNS, port, HTTP/HTTPS, and TCP checks              |
| 4     | Docker, Docker Compose | Package and run the application in containers                |
| 5     | AWS                    | Deploy OpsWatch to cloud infrastructure                      |
| 6     | Terraform              | Provision infrastructure as code                             |
| 7     | GitHub Actions         | Automate testing, building, and deployment                   |
| 8     | Prometheus, Grafana    | Collect metrics, visualize performance, and support alerting |
| 9     | Kubernetes             | Orchestrate containerized workloads                          |

This roadmap is a long-term plan, not a claim that all listed technologies are already implemented.

## 🏗️ Project Architecture

The intended architecture will evolve as new capabilities are introduced.

**Initial architecture:**

```text
User
  |
  v
OpsWatch CLI
  |
  +---- Service Checks
  |
  +---- URL Health Checks
  |
  +---- System Information
  |
  v
Health-Check Results
  |
  v
Local Log Files
```

**Long-term architecture:**

```text
Developer
    |
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    v
Docker Image
    |
    v
AWS Infrastructure
    |
    v
OpsWatch Application
    |
    +---- Health Checks
    +---- Metrics and Logs
    +---- Monitoring and Alerts
    |
    v
Prometheus + Grafana
```

Kubernetes and additional infrastructure components may be introduced when the application and learning objectives justify them.

## 📂 Project Structure

The initial project structure is expected to follow this organization:

```text
opswatch/
├── main.py
├── checker.py
├── system_info.py
├── logger.py
├── requirements.txt
├── README.md
└── logs/
```

| File or directory  | Responsibility                       |
| ------------------ | ------------------------------------ |
| `main.py`          | Application entry point and CLI menu |
| `checker.py`       | Service and URL health-check logic   |
| `system_info.py`   | System information collection        |
| `logger.py`        | Saving health-check results          |
| `requirements.txt` | External Python dependencies         |
| `logs/`            | Local health-check logs              |

The structure may change as the project grows. Modules will be introduced when their responsibilities become relevant.

## ⚙️ Getting Started

### Prerequisites

For the initial Python stage, you need:

- Python 3.10 or later.
- Git.
- A terminal or command-line interface.
- A code editor such as Visual Studio Code.

Some future features may require additional packages, permissions, or system dependencies.

### Installation

**1. Clone the repository**

Replace the placeholder below with the actual repository URL:

```bash
git clone https://github.com/wafiyu227/OpsWatch.git
```

**2. Navigate into the project directory**

```bash
cd opswatch
```

**3. Run the application**

Once the CLI entry point is implemented, launch it with:

```bash
python main.py
```

On some systems, you may need to use `python3 main.py` instead.

**Note:** These instructions describe the intended workflow. The application must have its entry point implemented before it can be run successfully.

## 🖥️ Usage

OpsWatch is intended to provide an interactive terminal interface.

The initial menu is planned to resemble the following:

```text
================================
          OpsWatch
================================

1. Check Service
2. Check URL
3. View System Information
4. Exit

Choose an option:
```

Users will select an option to initiate a check or view information. The menu will remain available until the user chooses to exit.

The service checks, URL checks, system reports, and logging functionality will become available as their respective milestones are completed.

## 🧪 Testing and Validation

Each feature will be validated before the next milestone begins.

Planned validation scenarios include:

- Valid and invalid user input.
- URLs that are reachable and unreachable.
- HTTP responses with different status codes.
- Network connection failures and timeouts.
- Service-running and service-stopped scenarios.
- Successful system information collection.
- Successful log creation and appending.
- Appropriate handling of unexpected errors.

Testing methods will expand to include automated Python tests, container tests, and CI/CD validation as the project matures.

## 🔐 Security Considerations

OpsWatch will progressively adopt security best practices, including:

- Avoiding hardcoded credentials and secrets.
- Using least-privilege permissions for application execution.
- Applying appropriate network access controls.
- Managing cloud permissions through IAM.
- Keeping dependencies documented and updated.
- Protecting logs from unauthorized access.
- Avoiding the unnecessary collection of sensitive system information.

## 🗺️ Development Roadmap

- [ ] **Stage 1:** Python CLI and health checks

  - [ ] Build the interactive CLI.
  - [ ] Implement service status checks.
  - [ ] Implement URL reachability checks.
  - [ ] Measure response times.
  - [ ] Collect basic system information.
  - [ ] Save health-check results to files.
  - [ ] Improve error handling and documentation.

- [ ] **Stage 2:** Linux administration and automation

  - [ ] Run OpsWatch on Linux.
  - [ ] Learn processes, users, permissions, and services.
  - [ ] Configure systemd.
  - [ ] Inspect logs and automate tasks with Bash.

- [ ] **Stage 3:** Networking

  - [ ] Add DNS resolution checks.
  - [ ] Add port and TCP connectivity checks.
  - [ ] Improve HTTP/HTTPS diagnostics.

- [ ] **Stage 4:** Containerization

  - [ ] Create a Dockerfile.
  - [ ] Build and run a Docker image.
  - [ ] Introduce Docker Compose.

- [ ] **Stage 5:** Cloud deployment

  - [ ] Deploy OpsWatch to AWS.
  - [ ] Configure networking and security.
  - [ ] Explore additional AWS services where appropriate.

- [ ] **Stage 6:** Infrastructure as Code

  - [ ] Recreate the AWS environment with Terraform.
  - [ ] Manage infrastructure changes through code.

- [ ] **Stage 7:** CI/CD

  - [ ] Automate testing with GitHub Actions.
  - [ ] Build and publish Docker images.
  - [ ] Automate deployment.

- [ ] **Stage 8:** Monitoring and observability

  - [ ] Expose application metrics.
  - [ ] Integrate Prometheus.
  - [ ] Create Grafana dashboards.
  - [ ] Configure alerts and improve log analysis.

- [ ] **Stage 9:** Kubernetes

  - [ ] Deploy OpsWatch to Kubernetes.
  - [ ] Explore deployments, services, configuration, and secrets.
  - [ ] Investigate health probes, scaling, and resource management.

## 🎓 Learning Philosophy

OpsWatch follows a project-based, incremental learning approach.

Each stage builds on the previous one, allowing new technologies to solve real problems within an existing application.

The guiding principles are:

- **Learn by building:** Apply concepts through practical implementation.
- **Understand before automating:** Learn the underlying systems before introducing automation.
- **Build incrementally:** Complete one milestone before moving to the next.
- **Practice troubleshooting:** Investigate failures instead of relying only on successful demonstrations.
- **Document progress:** Keep the project understandable, reproducible, and maintainable.
- **Avoid unnecessary complexity:** Introduce tools when the project has a clear need for them.

## 🤝 Contributions

OpsWatch is primarily a personal learning project. Suggestions, constructive feedback, and discussions about implementation choices are welcome.

If you would like to contribute, open an issue to discuss a proposed improvement before submitting substantial changes.

## 📄 License

No license has been selected yet. Until a license is added to the repository, others should not assume they have permission to redistribute or reuse the project's code.

A suitable open-source license can be added when the project is ready for public reuse.

## 👨‍💻 Author

**Ibrahim Wafiyudeen**

- GitHub: [@wafiyu227](https://github.com/wafiyu227)
- LinkedIn: [Ibrahim Wafiyudeen](https://linkedin.com/in/ibrahim-wafiyudeen-b07135344/)
- Portfolio: [ibrahimwafiyudeen-portfolio.netlify.app](https://ibrahimwafiyudeen-portfolio.netlify.app/)

---

*OpsWatch is a continuous learning project documenting the journey from Python development to Cloud/DevOps engineering, one milestone at a time.*
