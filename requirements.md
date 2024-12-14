# Prompt Generator Product Documentation

## Product Goals

Provide users with an efficient prompt generation, optimization, comparison, and evaluation tool that supports flexible task requirement definition, generates multiple prompt versions, and automatically evaluates and analyzes them to help users select the best solution.

---

## Interface Layout and Functional Modules

### 1. Left Sidebar: User Input Section

**Position**: Left side of the interface, occupying approximately 25% of the width.

**Functional Modules**:

1. **Task Description Input**:
   - Input field for users to describe task requirements or input their prompt.
   - Placeholder: `Enter task description, e.g., "Extract date and buyer email from order PDF", or input your prompt for optimization.`
   - Supports real-time content validation (checking for missing key information).

2. **Task Type Selection** (default is auto-select):
   - Dropdown menu for selecting task type:
     - Data Extraction
     - Decision Support
     - Content Generation
     - Data Analysis

3. **Language Model Selection**:
   - Dropdown menu: Select appropriate language model (e.g., Claude, GPT-4, PaLM).
   - Default recommendation: Automatically recommended based on task type and user preferences.

4. **Tone and Context**:
   - Dropdown menu: Select tone (Business, Friendly, Formal, etc.).
   - Scene input field: Input scene description (e.g., "Customer Support Scenario").

5. **Context Input**:
   - Input field for task context background information (e.g., "PDF contains order and customer information").
   - Placeholder: `Describe background context to help optimize generation...`

6. **Data Input (Optional)**:
   - Data field where users can paste or upload related data (supports JSON or CSV).
   - Example:
     ```json
     {
       "order_date": "2024-12-15",
       "buyer_name": "John Doe",
       "buyer_email": "john.doe@example.com"
     }
     ```

7. **Few-Shot Examples (Optional)**:
   - Input field for providing input and output examples.
   - Example:
     ```plaintext
     Input: PDF contains "Order Date: 2024-12-15"
     Output: {"order_date": "2024-12-15"}
     ```

**Action Buttons**:
- **Generate Button**:
  - Text: `Generate Prompt`
  - Function: Generates 3 prompt alternatives based on input content.
- **Optimize Button**:
  - Text: `Optimize Prompt`
  - Function: Optimizes the user's initial prompt.

---

### 2. Right Side: Prompt Comparison and Addition Section

**Position**: Upper right of the interface, occupying approximately 50% of the width.

**Functional Modules**:

#### **First Three Columns Functionality**
**Interactive Features**:
   - **Text Editing**: Supports direct modification by clicking on each section of the prompt.

1. **Prompt Naming**
   - Automatic code names generated from movies, music, or mythology.
   - **Version Management**:
     - Displays version number and timestamp.
     - Click dropdown next to prompt name to show version history list, supporting view and rollback.
   - **Favorite Function**:
     - Star icon next to prompt name for favorite marking.

2. **Prompt Alternative Display**:
   - Each prompt is presented with the following structured sections:
     - **Role**: Defines task role.
     - **Task**: Describes task objective.
     - **In-Prompt Context**: Shows supplementary context information.
     - **Rules & Constraints**: Shows task rules and limitations.
     - **Output Format**: Defines output structure.

 3. **Enhancements**:
   1. **Rich Context Integration**:
      - Tailor summaries and recommendations to user goals and data
      - Dynamically adapt to user preferences and historical interactions
      - Incorporate domain-specific knowledge and best practices
      - Support for multiple data sources and formats

   2. **Reasoning Generation**:
      - System automatically generates Reasoning section
      - User can manually adjust and refine reasoning
      - Transparent decision-making process
      - Step-by-step explanation of prompt logic

   3. **Actionable Outputs**:
      - Clear and implementable recommendations
      - Prioritized action items
      - Measurable success criteria
      - Follow-up suggestions and next steps

   4. **Edge Case Handling**:
      - Robust error detection and prevention
      - Graceful handling of unexpected inputs
      - Fallback strategies for incomplete data
      - Comprehensive validation checks

#### **Fourth Column: Search or Add**
- Provides 3 columns to display each alternative prompt, with the 4th column on the right for user search or prompt addition.

1. **Search Existing Templates**:
   - Search box where users can input keywords (e.g., "Email Onboarding Prompt").
   - Load search results from built-in template library or external platforms.
   - Search results include prompt name, compatibility, source (e.g., PromptBase).
   - Support "Preview" or "Apply".
2. **Add Favorites**:
   - Click "Add Favorite" button to open favorites popup.
   - Select prompt from favorites to add to comparison area.

---

### 3. Bottom Right: Evaluation and Analysis Section

**Position**: Lower right of the interface, occupying approximately 50% of the width.

**Functional Modules**:

#### **Evaluation and Analysis**
1. **Test**:
   - Function: Run prompt to generate actual task output.
   - Display generated output results for prompt performance verification.

2. **Evaluate**:
   - Display multi-dimensional evaluation results for prompt, including:
     - Accuracy
     - Efficiency (Token Usage)
     - Latency
     - Reasoning Coherence
   - Evaluation results shown in chart form (e.g., bar charts, radar charts).

3. **Validate**:
   - Function: Verify if prompt output complies with rules.
   - Display validation report, including rule compliance rate and error list.

4. **Train**:
   - Function: Users upload historical task data for training and optimizing prompt.
   - Display improvement points and metric changes after training.

#### **Comparison Analysis**
- **Compare Prompts**:
  - Display evaluation results for all prompts.
  - Support multi-dimensional comparison (accuracy, logic, etc.).
  - Generate comparison report, recommend optimal prompt.
- Example comparison table:
  | Prompt      | Accuracy | Token Usage | Latency | Logic | Overall Score |
  | ----------- | -------- | ----------- | ------- | ----- | ------------- |
  | Prompt_001  | 93%      | 1100        | 1.5s    | High  | 8.7          |
  | Prompt_002  | 95%      | 1200        | 1.8s    | High  | 9.2          |
  | Prompt_003  | 90%      | 1050        | 1.6s    | Med   | 8.5          |

---

## Interface Design Highlights

1. **Modular Layout**:
   - Left input section, right comparison and addition section, bottom evaluation section, clear functional zoning.

2. **Real-time Interaction**:
   - Supports structured section editing of prompts, real-time generation of reasoning and analysis results.

3. **Dynamic Extension**:
   - Search function integrates external platforms (e.g., PromptBase).
   - Favorite management and version rollback ensure prompt usability and controllability.

4. **Visual Analysis**:
   - Evaluation results displayed in chart form for easy user understanding and comparison.

---

This document provides detailed layout and interaction logic support for Prompt Generator's core functionality. If more detailed implementation or adjustments are needed, please feel free to ask!
