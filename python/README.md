\# AI Automotive Platform



A Python-based AI automotive diagnostic platform demonstrating the integration of a local Large Language Model (LLM) with structured data validation, API orchestration, PostgreSQL persistence, and automated testing.



The project was developed as a practical AI and automation engineering project to demonstrate how AI-generated information can be converted into structured, validated data and processed through a reliable software workflow.



\---



\## Project Overview



The AI Automotive Platform processes customer-reported vehicle information and uses a local LLM to extract structured information from natural-language responses.



The platform combines:



\- Python

\- Local Qwen LLM

\- Pydantic

\- FastAPI

\- PostgreSQL

\- Docker

\- pytest

\- HTTP API integration

\- Structured data validation

\- Database persistence

\- Automated testing



The project focuses on building an AI workflow that is \*\*structured, testable, observable, and designed to fail safely when AI-generated information cannot be validated\*\*.



\---



\## What This Project Demonstrates



This project demonstrates practical experience in:



\- Integrating a local LLM into a Python application

\- Extracting structured information from natural-language customer messages

\- Validating AI-generated output using Pydantic models

\- Applying strict validation rules to AI responses

\- Building REST APIs with FastAPI

\- Designing multi-step diagnostic workflows

\- Persisting validated information in PostgreSQL

\- Handling AI extraction failures safely

\- Handling database failures safely

\- Implementing request IDs for API traceability

\- Recording API processing time

\- Writing unit, API and integration tests

\- Testing real database persistence

\- Working with Docker-based infrastructure

\- Diagnosing and resolving local integration issues

\- Using Git and GitHub for source control



\---



\## High-Level Architecture



```text

Customer Message

&#x20;      |

&#x20;      v

&#x20;FastAPI API

&#x20;      |

&#x20;      +----------------------+

&#x20;      |                      |

&#x20;      v                      v

Diagnostic Workflow     Evidence Extraction

&#x20;      |                      |

&#x20;      v                      v

Local Qwen LLM          Local Qwen LLM

&#x20;      |                      |

&#x20;      v                      v

Pydantic Validation     Pydantic Validation

&#x20;      |                      |

&#x20;      v                      v

Updated Diagnostic     Validated Evidence

Facts                       |

&#x20;      |                      v

&#x20;      v                 PostgreSQL

Next Question                 |

&#x20;                             v

&#x20;                        Record ID

