export interface Documentation {
  Overview: OverviewSection;
  GettingStarted: GettingStartedSection;
  CodeStructureOverview: CodeStructureOverviewSection;
  KeyCodeComponents: KeyCodeComponentsSection;
  FunctionsAndAPIDocumentation: FunctionsAndAPIDocumentationSection;
  ErrorHandlingAndLogging: ErrorHandlingAndLoggingSection;
  Dependencies: DependenciesSection;
  Configuration: ConfigurationSection;
  PerformanceConsiderations: PerformanceConsiderationsSection;
  TestingAndQualityAssurance: TestingAndQualityAssuranceSection;
  SecurityConsiderations: SecurityConsiderationsSection;
  VersionControlAndChangelog: VersionControlAndChangelogSection;
  FAQ: FAQSection;
  Appendix: AppendixSection;
  Conclusion: ConclusionSection;
}

// Section: Overview
export interface OverviewSection {
  description: string;
}

// Section: Getting Started
export interface GettingStartedSection {
  Prerequisites: string[];
  SetupInstructions: string[];
  RunInstructions: string[];
  ExampleUsage: string[];
}

// Section: Code Structure Overview
export interface CodeStructureOverviewSection {
  FileOrganization: FileOrganizationItem[];
  ModuleBreakdown: Record<string, string>;
}

export interface FileOrganizationItem {
  name: string;
  type: 'file' | 'folder';
  children?: FileOrganizationItem[];
}

// Section: Key Code Components
export interface KeyCodeComponentsSection {
  Classes: ClassDetail[];
  DataStructures: DataStructureDetail[];
}

export interface ClassDetail {
  className: string;
  description: string;
  constructors: ConstructorDetail[];
  methods: MethodDetail[];
}

export interface ConstructorDetail {
  parameters: ParameterDetail[];
  description: string;
}

export interface MethodDetail {
  methodName: string;
  parameters: ParameterDetail[];
  returnType: string;
  description: string;
  exampleUsage: string;
}

export interface ParameterDetail {
  name: string;
  type: string;
  description: string;
}

export interface DataStructureDetail {
  name: string;
  type: string;
  purpose: string;
  assumptions: string[];
}

// Section: Functions and API Documentation
export interface FunctionsAndAPIDocumentationSection {
  Functions: FunctionDetail[];
  APIEndpoints: APIEndpointDetail[];
}

export interface FunctionDetail {
  functionName: string;
  signature: string;
  description: string;
  exampleInput: string;
  exampleOutput: string;
  sideEffects: string;
}

export interface APIEndpointDetail {
  endpoint: string;
  method: string;
  description: string;
  parameters: APIParameter[];
  response: APIResponseDetail;
}

export interface APIParameter {
  name: string;
  type: string;
  required: boolean;
  description: string;
}

export interface APIResponseDetail {
  statusCodes: string[];
  dataFormat: string;
  exampleResponse: string;
}

// Section: Error Handling and Logging
export interface ErrorHandlingAndLoggingSection {
  ExceptionHandling: string;
  ErrorCodes: ErrorCode[];
  Logging: string;
}

export interface ErrorCode {
  code: string;
  description: string;
}

// Section: Dependencies
export interface DependenciesSection {
  ExternalLibraries: ExternalLibrary[];
  InternalDependencies: string[];
}

export interface ExternalLibrary {
  library: string;
  version: string;
}

// Section: Configuration
export interface ConfigurationSection {
  ConfigurationFiles: ConfigurationFile[];
  EnvironmentVariables: EnvironmentVariable[];
}

export interface ConfigurationFile {
  name: string;
  description: string;
}

export interface EnvironmentVariable {
  variable: string;
  description: string;
}

// Section: Performance Considerations
export interface PerformanceConsiderationsSection {
  Optimizations: string[];
  Scalability: string;
  Benchmarks?: string[];
}

// Section: Testing and Quality Assurance
export interface TestingAndQualityAssuranceSection {
  TestingStrategy: string;
  TestCoverage: string;
  TestCases: TestCase[];
  Tools: string[];
}

export interface TestCase {
  description: string;
  expectedInput: string;
  expectedOutput: string;
}

// Section: Security Considerations
export interface SecurityConsiderationsSection {
  SensitiveDataHandling: string;
  AccessControl: string;
  Vulnerabilities: string[];
}

// Section: Version Control and Changelog
export interface VersionControlAndChangelogSection {
  GitHistory: string;
  Changelog: string[];
}

// Section: FAQ
export interface FAQSection {
  CommonQuestions: string[];
  Troubleshooting: TroubleshootingTip[];
}

export interface TroubleshootingTip {
  issue: string;
  solution: string;
}

// Section: Appendix
export interface AppendixSection {
  Glossary: GlossaryTerm[];
  References: string[];
}

export interface GlossaryTerm {
  term: string;
  definition: string;
}

// Section: Conclusion
export interface ConclusionSection {
  Summary: string;
  NextSteps: string;
}
