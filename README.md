<p align="center">
  <img src="assets/MEGATRON.png" alt="Megatron" width="280"/>
</p>

<h1 align="center">Megatron — DevSecOps & Supply Chain Security</h1>

<p align="center">
  <em>As one of the most powerful villains, Megatron enforces an automated Shift-Left Security supply-chain pipeline designed to guarantee artifact provenance, repository hygiene, and vulnerability transparency across every stage of the software lifecycle.</em>
</p>

---

### Pipeline Flow
```text
Code & Pinning ──> OpenSSF Hygiene ──> Syft (SBOM) ──> Grype (SARIF) ──> Trivy Audit ──> Cosign (Keyless)
```

### 1. Automated SBOM & CVE Tracking
- **Standard:** Generates **CycloneDX v1.7 (JSON)** via **Anchore Syft** on every push/PR.
- **Vulnerability Scanning:** **Anchore Grype** parses the SBOM against NVD and GitHub Security Advisories.
- **Security Dashboard:** Automatically exports OASIS SARIF alerts directly to **GitHub Security -> Code scanning alerts**.

### 2. Repository Hygiene & OpenSSF Scorecards
- **Dependency Pinning:** All GitHub Actions workflows and Docker base images are pinned to immutable **40-character Commit SHAs** and cryptographic digests to prevent *Tag Hijacking*.
- **Branch Protection:** Enforced PR reviews, required status checks, and disabled force-pushes on `main`.

### 3. Multi-Layer Security Audit
- **Security Trivy** runs a three-tier QA gate:
  1. **Filesystem & Config:** Scans source code for leaked secrets, misconfigurations, and IaC flaws.
  2. **SBOM Cross-Check:** Correlates Syft's output against Trivy's vulnerability database.
  3. **Container Image:** Evaluates base OS layers and language runtime packages.

---