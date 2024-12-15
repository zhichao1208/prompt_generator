# Prompt Generator Requirements

## Overview
A comprehensive prompt engineering and evaluation system that helps users create, optimize, and compare different prompt solutions for various AI tasks. The system provides detailed analysis, visualization, and performance metrics for each solution.

## Core Features

### Task Configuration

#### Task Description
A free-text input field where users can describe their specific requirements. This serves as the foundation for generating targeted prompts that precisely match the user's needs.

#### Task Type Selection 
Categorizes the task to optimize prompt generation and model selection:
- **Recommended**: System automatically suggests the best task type based on description
- **Data Extraction**: For tasks involving pulling specific information from documents
- **Decision Support**: For tasks requiring analysis and decision-making assistance
- **Content Generation**: For tasks involving creating new content
- **Data Analysis**: For tasks focused on analyzing and interpreting data

### Model Selection

#### Model Categories
Different AI models optimized for various use cases:
- **Recommended**: System-selected optimal model based on task requirements
- **Claude**: Anthropic's models known for reasoning and analysis
  - opus: Most powerful, best for complex tasks
  - sonnet: Balanced performance and efficiency
  - haiku: Fast, efficient for simple tasks
- **GPT**: OpenAI's models with varying capabilities
  - 3.5-turbo: Fast and cost-effective
  - 4: Enhanced reasoning and accuracy
  - 4-turbo: Latest capabilities with improved performance
- **Other**: Alternative models for specific needs
  - gemini-pro: Google's advanced model
  - mixtral: Open-source alternative
  - llama-2: Meta's powerful open model

#### Multiple Model Support
Enables comparison of different models' performance on the same task, helping users make informed decisions about which model best suits their needs.

#### Version Control
Tracks changes and maintains history of prompt iterations, allowing users to compare versions and roll back if needed.

### Input Configuration

#### Tone and Context
Customization options for output style and background information:
- **Communication Tone**:
  - Professional: Formal business communication
  - Friendly: Casual, approachable style
  - Formal: Strictly professional and academic
  - Casual: Relaxed, conversational tone

#### Context Information
Additional background details that help models better understand the task environment and requirements.

#### Sample Data Input
Example data that helps models understand the expected input format and content structure.

#### Few-Shot Examples
Real examples of input-output pairs that guide the model in understanding the desired behavior.

### Solution Comparison

#### Solution Display
Three distinct approaches to solving the task:
- **JARVIS**: Comprehensive solution focusing on accuracy and completeness
- **SHERLOCK**: Balanced approach emphasizing validation and reliability
- **FLASH**: Speed-optimized solution for quick results

#### Quick Actions
Convenient buttons for common operations:
- **Favorite (⭐)**: Save preferred solutions for future reference
- **Import (📥)**: Bring in solutions from external sources
- **Search (🔍)**: Find similar solutions in the database

### Evaluation & Analysis

#### Test & Results
Comprehensive testing capabilities:
- **Test Input**: Upload and process real data
- **Results Display**: Clear presentation of outcomes
- **Performance Metrics**: Detailed success measurements

#### Core Metrics
Key performance indicators:
- **Accuracy**: Correctness of extracted information
- **Goal Achievement**: Task completion rate
- **Efficiency**: Resource usage optimization
- **Logic Score**: Quality of reasoning process

#### Advanced Dimensions
Detailed performance aspects:
- **Stability**: Reliability across different scenarios
- **Explainability**: Clarity of decision-making process
- **Creativity**: Ability to handle unique situations
- **Safety**: Security and compliance measures

### Weight Configuration
Customizable importance of different metrics:
- **Core Weights**: Adjust primary metric importance
- **Advanced Weights**: Fine-tune specialized metrics

### Enhancement Features

#### Dynamic Prompt Optimization
Continuous improvement capabilities:
- **Examples Management**: Build and maintain training data
- **Edge Cases**: Handle exceptional situations
- **Performance Tuning**: Optimize for specific needs

#### Model Settings
Fine-grained control over model behavior:
- **Temperature**: Control output randomness
- **Top P**: Manage response diversity
- **Max Tokens**: Set output length limits
- **Frequency Penalty**: Avoid repetitive content

## Performance Standards
Specific targets for quality assurance:
- **Accuracy**: Minimum 90% correct results
- **Response Time**: Optimized for each solution type
- **Cost Efficiency**: Balanced performance and resource usage

## Technical Implementation
Key technical requirements:
- **Streamlit**: Modern web interface
- **Plotly**: Interactive visualizations
- **Version Control**: Change management
- **Error Handling**: Robust error management
- **Cross-browser**: Wide compatibility

## Implementation Examples

### Sample Task Configuration
```plaintext
Task Description: "Extract order date, buyer name and email address from my order pdf"
Task Type: Data Extraction
Selected Models: GPT-4-turbo (Recommended)
```

### Sample Data Input
```plaintext
Order Details
Date: 2024-03-20
Customer Information:
Name: John Smith
Email: john.smith@example.com
Order Number: ORD-2024-001
```

### Solution Examples

#### JARVIS Solution
```plaintext
Introduction:
- Comprehensive Approach
- Complete data validation and error handling
- Resource Consumption: high

Role:
You are a highly skilled Data Extraction Specialist, adept at analyzing unstructured data like emails and attachments to extract accurate and relevant information. Your role involves ensuring all required fields are captured with precision, adhering to strict rules, and providing reasoning for any ambiguities encountered during extraction.

Task:
Your task is to extract order-related information from an email and its attachments. The email was sent by a customer to the seller. You will process this data for TechHeroes to fulfill the order accurately.

Rules & Constraints:
1. General Rules
   Accuracy First:
   - Extract only explicitly stated information
   - Do not infer or generate information that is not directly present
   - Validate all extracted data against defined rules
   - Document any assumptions or decisions made

2. Missing Data Handling:
   - For missing required fields, use "unknown" as the value
   - Log all missing fields for review
   - Provide explanation for why data couldn't be extracted
   - Suggest potential data sources or alternatives

3. Email Address Validation:
   - Must belong to an individual (e.g., john.doe@example.com)
   - Reject generic addresses (e.g., info@, sales@, support@)
   - Verify email format compliance
   - Check domain validity

4. Article Code Processing:
   - Extract only the seller's (TechHeroes) product_n_article_code
   - Remove special characters (., -, ) for continuous alphanumeric string
   - Present multiple codes as comma-separated list
   - Maintain original code reference for traceability

5. Output Format Consistency:
   - Follow predefined JSON structure
   - Include all mandatory fields
   - Add metadata for processing details
   - Include confidence scores for extracted data

Reasoning Method:
Chain-of-Thought (CoT)
- Step-by-step analysis of document structure
- Explicit documentation of decision points
- Clear reasoning path for validation
- Traceable extraction process

Planning Method:
Least-to-Most Decomposition
- Break down complex documents into sections
- Process each field with specific rules
- Combine results with validation
- Generate comprehensive output

Context:
Background:
- TechHeroes is an e-commerce company specializing in tech products
- They receive orders through email and various document formats
- The system needs to process both direct customer emails and forwarded messages
- High accuracy requirements for order processing

Technical Environment:
- Email server supports IMAP/POP3 protocols
- Document processing system handles PDF, DOC, and image formats
- Integration with order management system required
- Compliance with data protection regulations

Output Format:
{
  "metadata": {
    "version": "1.0",
    "timestamp": "YYYY-MM-DD HH:mm:ss",
    "processor": "JARVIS",
    "confidence_score": 0.95
  },
  "order": {
    "order_number": "string",
    "order_date": "YYYY-MM-DD",
    "status": "string"
  },
  "customer": {
    "name": {
      "full_name": "string",
      "first_name": "string",
      "last_name": "string"
    },
    "email": "string",
    "validation": {
      "email_valid": boolean,
      "name_complete": boolean
    }
  },
  "products": [
    {
      "code": "string",
      "quantity": number,
      "original_code": "string"
    }
  ],
  "processing": {
    "missing_fields": ["field1", "field2"],
    "warnings": ["warning1", "warning2"],
    "notes": ["note1", "note2"]
  }
}
```

#### SHERLOCK Solution
```plaintext
Introduction:
- Validation Focus
- Strong error detection and correction
- Resource Consumption: medium

Role:
You are a Data Validation Expert specializing in PDF document analysis and structured information extraction. Your focus is on maintaining data accuracy, implementing robust validation rules, and ensuring data consistency across different document formats. You excel at pattern recognition and data standardization.

Task:
Your primary task is to extract and validate three key pieces of information from PDF documents:
1. Order date - Must be in a valid date format
2. Buyer name - Full name of the customer
3. Email address - Must be a valid individual email address

Rules & Constraints:
1. Field Validation
   Date Validation:
   - Must be a valid date within the last 30 days
   - Convert all formats to YYYY-MM-DD
   - Handle various input formats (MM/DD/YYYY, DD-MM-YYYY, etc.)
   - Validate against business calendar

   Name Validation:
   - Must contain both first and last name
   - Capitalize first letter of each word
   - Remove unnecessary spaces or characters
   - Check against common name patterns

   Email Validation:
   - Must be individual email (not generic/group address)
   - Convert to lowercase
   - Verify format and domain
   - Check against blocked domains list

2. Processing Rules
   Document Analysis:
   - Scan full document for relevant sections
   - Identify data patterns and structures
   - Map fields to standard format
   - Track data source locations

   Error Handling:
   - Log all validation failures
   - Provide specific error messages
   - Suggest corrections
   - Track error patterns

3. Quality Assurance
   Data Verification:
   - Cross-reference extracted data
   - Check for consistency
   - Validate against business rules
   - Generate quality scores

Reasoning Method:
ReAct (Reasoning + Acting)
- Observe document structure
- Think about extraction strategy
- Act on identified patterns
- Reflect on results

Planning Method:
Plan-and-Solve Strategy
- Analyze document layout
- Identify data locations
- Execute extraction plan
- Validate results

Context:
Processing Environment:
- PDF processing system with OCR capabilities
- Regular document structure updates
- High volume of daily orders
- Strict accuracy requirements

Technical Setup:
- OCR engine for text extraction
- Pattern matching algorithms
- Validation rule engine
- Error correction system

Output Format:
{
  "validation_result": {
    "status": "success|error",
    "timestamp": "YYYY-MM-DD HH:mm:ss",
    "version": "1.0"
  },
  "extracted_data": {
    "order_date": {
      "value": "YYYY-MM-DD",
      "original_format": "string",
      "confidence": number
    },
    "buyer_name": {
      "value": "string",
      "components": {
        "first_name": "string",
        "last_name": "string"
      },
      "confidence": number
    },
    "email": {
      "value": "string",
      "validation": {
        "format_valid": boolean,
        "domain_valid": boolean
      },
      "confidence": number
    }
  },
  "validation_details": {
    "checks_performed": ["check1", "check2"],
    "warnings": ["warning1", "warning2"],
    "suggestions": ["suggestion1", "suggestion2"]
  },
  "quality_metrics": {
    "overall_confidence": number,
    "validation_score": number,
    "completeness_score": number
  }
}
```

#### FLASH Solution
```plaintext
Introduction:
- Lightweight Design
- Fast processing speed
- Resource Consumption: low

Role:
You are a Focused Data Parser with expertise in minimal, targeted information extraction. Your specialty lies in quickly identifying and extracting specific data points from documents while maintaining high accuracy. You excel at efficient processing and streamlined output generation.

Task:
Your task is to perform targeted extraction of three essential fields from PDF documents:
1. Order date
2. Buyer name
3. Email address

Rules & Constraints:
1. Extraction Focus
   Primary Rules:
   - Extract only the three required fields
   - Skip all other information
   - No complex validation required
   - Maintain extraction speed

   Processing Limits:
   - Single-pass extraction only
   - Minimal pattern matching
   - Basic format checking
   - Quick validation rules

2. Basic Formatting
   Date Handling:
   - Convert to YYYY-MM-DD
   - Simple format recognition
   - Basic validity check
   - Skip complex date parsing

   Name Processing:
   - Keep original format
   - Basic cleanup only
   - Maintain case as found
   - No complex normalization

   Email Handling:
   - Convert to lowercase
   - Basic format check
   - No detailed validation
   - Quick pattern matching

3. Performance Rules
   Optimization:
   - Minimize processing steps
   - Reduce validation complexity
   - Quick pattern matching
   - Early exit on success

   Resource Usage:
   - Limit memory usage
   - Minimize CPU cycles
   - Reduce I/O operations
   - Optimize for speed

Reasoning Method:
Tree-of-Thought (ToT)
- Quick path identification
- Minimal branching
- Fast decision making
- Streamlined processing

Planning Method:
Progressive Task Refinement
- Quick document scan
- Direct field extraction
- Basic validation
- Fast output generation

Context:
Processing Setup:
- Basic PDF text extraction
- Single-thread processing
- Minimal memory usage
- Speed-optimized workflow

Technical Environment:
- Basic text parser
- Minimal dependencies
- Lightweight processing
- Quick response time

Output Format:
{
  "data": {
    "date": "YYYY-MM-DD",
    "name": "string",
    "email": "string"
  },
  "stats": {
    "processing_time_ms": number,
    "fields_found": number
  }
}
```

### Example Test Cases

#### Standard Examples
1. **Example 1**:
```plaintext
Input:
Email Content:
Subject: Order Confirmation #12345
From: john.smith@company.com
Date: 2024-03-15

Dear TechHeroes,
Please process my order #TH-2024-12345.
Shipping Address: 123 Main St, Boston, MA 02108

Output:
{
  "order_number": "TH202412345",
  "buyer_email": "john.smith@company.com",
  "order_date": "2024-03-15",
  "shipping_address": {
    "street": "123 Main St",
    "city": "Boston",
    "state": "MA",
    "zip": "02108"
  }
}
```

2. **Example 2**:
```plaintext
Input:
Attachment: invoice.pdf
Order: #TH-2024-56789
Customer: Jane Doe (jane.doe@email.com)
Products:
- 2x TH-PRD-001 ($99.99 each)
- 1x TH-PRD-002 ($149.99)

Output:
{
  "order_number": "TH202456789",
  "buyer_email": "jane.doe@email.com",
  "products": [
    {
      "code": "THPRD001",
      "quantity": 2,
      "price": 99.99
    },
    {
      "code": "THPRD002",
      "quantity": 1,
      "price": 149.99
    }
  ]
}
```

#### Edge Cases
1. **Invalid Email Format**:
```plaintext
Case: Invalid Email Format
Input:
From: sales@company.com
Order: #TH-2024-99999
Customer: Alice Johnson

Handling:
{
  "error": "Invalid email format",
  "details": "Generic email address not allowed (sales@company.com)",
  "required": "Individual email address (e.g., firstname.lastname@company.com)"
}
```

2. **Multiple Order Numbers**:
```plaintext
Case: Multiple Order Numbers
Input:
Reference: #TH-2024-11111
Original Order: #TH-2024-22222
Updated Order: #TH-2024-33333

Handling:
{
  "current_order": "TH202433333",
  "original_order": "TH202422222",
  "reference_order": "TH202411111",
  "note": "Using most recent order number as primary reference"
}
```

3. **Inconsistent Date Formats**:
```plaintext
Case: Inconsistent Date Formats
Input:
Order Date: 03/15/2024
Delivery: 2024-04-01
Expected: 1st May 2024

Handling:
{
  "order_date": "2024-03-15",
  "delivery_date": "2024-04-01",
  "expected_date": "2024-05-01",
  "note": "All dates normalized to YYYY-MM-DD format"
}
```

### Advanced Configuration Examples

#### Model Settings Examples
1. **JARVIS Configuration**:
```plaintext
Temperature: 0.7
Top P: 0.9
Max Tokens: 2048
Frequency Penalty: 0.0

Rationale:
- Using GPT-4 Turbo for superior performance in structured data extraction
- Optimized for accuracy and consistency in field identification
- Perfect match for PDF parsing and data normalization
- Strong capability in handling multiple date formats
- Excellent at email validation and formatting
```

2. **SHERLOCK Configuration**:
```plaintext
Temperature: 0.6
Top P: 0.85
Max Tokens: 1800
Frequency Penalty: 0.1

Rationale:
- Using GPT-4 Turbo for robust validation capabilities
- Excellent at pattern recognition and error detection
- Specialized in data validation and standardization
- Strong in identifying format inconsistencies
- Built-in error correction suggestions
```

3. **FLASH Configuration**:
```plaintext
Temperature: 0.5
Top P: 0.8
Max Tokens: 1500
Frequency Penalty: 0.2

Rationale:
- Using GPT-4 Turbo for precise extraction capabilities
- Focused on efficiency and accuracy
- Specialized in key field extraction
- Minimal but essential validation
- Streamlined processing
```

### Evaluation Results Examples

#### Core Metrics Comparison
```plaintext
JARVIS:
- Accuracy: 98% 
- Goal Achievement: 100%
- Efficiency: 95%
- Logic Score: 97%

SHERLOCK:
- Accuracy: 95%
- Goal Achievement: 98%
- Efficiency: 97%
- Logic Score: 96%

FLASH:
- Accuracy: 92%
- Goal Achievement: 95%
- Efficiency: 99%
- Logic Score: 93%
```

#### Efficiency Breakdown Details
```plaintext
JARVIS:
- Token Usage: 2,500 tokens
- Response Time: 2.5s
- Cost per Run: $0.05

SHERLOCK:
- Token Usage: 1,800 tokens
- Response Time: 1.8s
- Cost per Run: $0.035

FLASH:
- Token Usage: 1,200 tokens
- Response Time: 1.2s
- Cost per Run: $0.025
```

#### Advanced Dimensions Results

##### JARVIS Advanced Metrics
```plaintext
Stability Analysis:
- Format Compatibility: 96%
- Error Handling: 98%
- Cross-platform: 95%
- System Stability: 97%

Explainability:
- Process Transparency: 98%
- Decision Clarity: 97%
- Documentation: 96%
- Reasoning Path: 95%

Creativity & Adaptability:
- Pattern Recognition: 94%
- Format Flexibility: 93%
- Edge Case Handling: 92%
- Learning Ability: 91%

Safety & Compliance:
- Data Protection: 99%
- Bias Prevention: 98%
- Compliance: 97%
- Risk Control: 96%
```

##### SHERLOCK Advanced Metrics
```plaintext
Stability Analysis:
- Format Compatibility: 97%
- Error Handling: 96%
- Cross-platform: 97%
- System Stability: 97%

Explainability:
- Process Transparency: 96%
- Decision Clarity: 95%
- Documentation: 97%
- Reasoning Path: 95%

Creativity & Adaptability:
- Pattern Recognition: 92%
- Format Flexibility: 91%
- Edge Case Handling: 93%
- Learning Ability: 91%

Safety & Compliance:
- Data Protection: 98%
- Bias Prevention: 97%
- Compliance: 98%
- Risk Control: 96%
```

##### FLASH Advanced Metrics
```plaintext
Stability Analysis:
- Format Compatibility: 94%
- Error Handling: 93%
- Cross-platform: 92%
- System Stability: 90%

Explainability:
- Process Transparency: 91%
- Decision Clarity: 92%
- Documentation: 90%
- Reasoning Path: 89%

Creativity & Adaptability:
- Pattern Recognition: 88%
- Format Flexibility: 87%
- Edge Case Handling: 87%
- Learning Ability: 86%

Safety & Compliance:
- Data Protection: 96%
- Bias Prevention: 95%
- Compliance: 94%
- Risk Control: 93%
```

### Test Results Examples

#### JARVIS Test Output
```plaintext
Planning:
1. Document Analysis
   - Parse PDF structure
   - Identify key sections
   - Map target fields

2. Field Extraction
   - Date patterns
   - Name formats
   - Email validation

3. Data Validation
   - Format check
   - Completeness verify
   - Error handling

Reasoning:
Using Chain-of-Thought:
1. Located order section
2. Found date: 2024-03-20
3. Identified customer info block
4. Extracted name: John Smith
5. Validated email format
6. Confirmed: john.smith@example.com

Output:
{
  "order_date": "2024-03-20",
  "buyer_name": "John Smith",
  "email": "john.smith@example.com",
  "confidence_score": 0.95
}
```

#### SHERLOCK Test Output
```plaintext
Planning:
1. Initial Scan
   - Document structure check
   - Field location mapping
   - Validation rules setup

2. Data Processing
   - Pattern matching
   - Format validation
   - Error detection

3. Quality Control
   - Data verification
   - Format standardization
   - Completeness check

Reasoning:
Using ReAct:
1. PDF scan complete
2. Date found: 2024-03-20
3. Name section identified
4. Name extracted: John Smith
5. Email located and validated
6. Email confirmed: john.smith@example.com

Output:
{
  "extracted_data": {
    "date": "2024-03-20",
    "name": "John Smith",
    "email": "john.smith@example.com"
  },
  "validation": {
    "all_fields_found": true,
    "formats_valid": true
  }
}
```

#### FLASH Test Output
```plaintext
Planning:
1. Quick Scan
   - Target field search
   - Direct extraction
   - Basic validation

2. Processing
   - Simple pattern match
   - Format check
   - Data extraction

Reasoning:
Using Tree-of-Thought:
1. Scanned document
2. Found date: 2024-03-20
3. Extracted name: John Smith
4. Found email: john.smith@example.com
5. Basic validation passed

Output:
{
  "date": "2024-03-20",
  "name": "John Smith",
  "email": "john.smith@example.com"
}
```
