# Research: Todo AI Chatbot Implementation

## Executive Summary

This research document outlines the technical decisions and approaches for implementing the Todo AI Chatbot feature, focusing on integrating natural language processing with existing todo management functionality.

## Decision: MCP Tool Architecture
**Rationale**: Aligns with the constitutional requirement that "AI must act only through MCP tools" and provides a clean separation between AI reasoning and system operations. MCP tools ensure all actions are traceable, auditable, and secure.

**Alternatives considered**:
- Direct database operations from AI agent: Violates constitution principle
- REST API calls from AI agent: Less secure and harder to audit than MCP tools
- Custom RPC mechanism: Would require building additional infrastructure

## Decision: Existing Chatbot Skill Integration
**Rationale**: The existing chatbot skill from `/home/zain/.claude/skills/my_skills/chatbot.md` provides a proven RAG-based architecture that can be adapted for the todo domain. This reduces development time and leverages established patterns for conversation management and intent detection.

**Alternatives considered**:
- Building from scratch: Higher development overhead and risk
- Different chatbot frameworks: Would require learning curve and potential compatibility issues
- Third-party chatbot services: Less control and potential cost concerns

## Decision: FastAPI Backend Framework
**Rationale**: Aligns with the architectural rule "FastAPI handles HTTP only" and integrates well with the existing Python ecosystem. FastAPI provides excellent async support, automatic API documentation, and strong type validation.

**Alternatives considered**:
- Flask: Less modern and lacks built-in async support
- Django: Overkill for this API-focused use case
- Node.js/Express: Would introduce different language ecosystem

## Decision: SQLModel for Database Operations
**Rationale**: Complies with constitutional requirement "MCP tools persist all state via SQLModel" and provides a Pydantic-compatible ORM that integrates well with FastAPI. Supports the "Database is the single source of truth" principle.

**Alternatives considered**:
- SQLAlchemy Core: More complex setup
- Peewee: Less Pydantic integration
- Tortoise ORM: Async-only, might complicate existing sync operations

## Decision: OpenAI Agents SDK for AI Reasoning
**Rationale**: Aligns with the architectural rule "OpenAI Agents SDK handles reasoning" and provides enterprise-grade tools for creating AI agents with function calling capabilities. Integrates well with MCP tools architecture.

**Alternatives considered**:
- LangChain: More general purpose, less focused on tool-based interactions
- Custom OpenAI API implementation: More development overhead
- Anthropic Claude: Would require different integration approach

## Decision: Frontend Chat Widget Integration
**Rationale**: Enables seamless integration with existing UI while providing dedicated chat functionality. The floating widget approach allows users to access chat from any page without leaving their current context.

**Alternatives considered**:
- Separate chat page: Would fragment user experience
- Inline commands in existing UI: Would clutter the existing interface
- Modal overlay: Less convenient for extended conversations

## Decision: Authentication via Better Auth
**Rationale**: Aligns with security rule "Authentication handled via Better Auth" and maintains consistency with existing authentication system. Provides user scoping required by "All operations are scoped by user_id".

**Alternatives considered**:
- Custom authentication: Would require additional development and security considerations
- Third-party OAuth providers: Would complicate existing auth flow
- Session-based auth: Less stateless than Better Auth approach

## Technology Stack Compatibility

The chosen architecture ensures compatibility between all components:
- Frontend React components communicate with FastAPI backend
- FastAPI integrates with Better Auth for user verification
- OpenAI Agents SDK interacts with MCP tools
- MCP tools connect to SQLModel database layer
- All components are containerizable for deployment