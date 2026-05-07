-- =====================================================
-- Predictive Insurance Platform
-- Physical Database Schema
-- CSE 4701 - Project Part 4
-- Emma Adams
-- =====================================================

-- =====================================================
-- DROP TABLES (Optional for Resetting Database)
-- =====================================================

DROP TABLE IF EXISTS RISK_ASSESSMENT;
DROP TABLE IF EXISTS RAW_DATASET;
DROP TABLE IF EXISTS DATA_SOURCE;
DROP TABLE IF EXISTS DOCUMENT;
DROP TABLE IF EXISTS COMMISSION;
DROP TABLE IF EXISTS ACTIVITY;
DROP TABLE IF EXISTS CONTRACT;
DROP TABLE IF EXISTS INTERACTION;
DROP TABLE IF EXISTS PRODUCT;
DROP TABLE IF EXISTS PRODUCT_TYPE;
DROP TABLE IF EXISTS CONTRACT_STATUS;
DROP TABLE IF EXISTS ACTIVITY_TYPE;
DROP TABLE IF EXISTS DOCUMENT_TYPE;
DROP TABLE IF EXISTS INTERACTION_MEDIUM;
DROP TABLE IF EXISTS FINANCIAL_PROFESSIONAL;
DROP TABLE IF EXISTS CONTRACT_HOLDER;
DROP TABLE IF EXISTS PROSPECT;
DROP TABLE IF EXISTS EMPLOYEE;
DROP TABLE IF EXISTS FIRM;
DROP TABLE IF EXISTS CLEARINGHOUSE;
DROP TABLE IF EXISTS PARTY;

-- =====================================================
-- PARTY TABLES
-- =====================================================

CREATE TABLE PARTY (
    PartyId INT PRIMARY KEY IDENTITY(1,1),
    Name VARCHAR(100) NOT NULL,
    Address VARCHAR(255),
    Email VARCHAR(100),
    Phone VARCHAR(25)
);

CREATE TABLE FINANCIAL_PROFESSIONAL (
    PartyId INT PRIMARY KEY,
    FOREIGN KEY (PartyId) REFERENCES PARTY(PartyId)
);

CREATE TABLE CONTRACT_HOLDER (
    PartyId INT PRIMARY KEY,
    FOREIGN KEY (PartyId) REFERENCES PARTY(PartyId)
);

CREATE TABLE PROSPECT (
    PartyId INT PRIMARY KEY,
    FOREIGN KEY (PartyId) REFERENCES PARTY(PartyId)
);

CREATE TABLE EMPLOYEE (
    PartyId INT PRIMARY KEY,
    FOREIGN KEY (PartyId) REFERENCES PARTY(PartyId)
);

CREATE TABLE FIRM (
    PartyId INT PRIMARY KEY,
    FOREIGN KEY (PartyId) REFERENCES PARTY(PartyId)
);

CREATE TABLE CLEARINGHOUSE (
    PartyId INT PRIMARY KEY,
    FOREIGN KEY (PartyId) REFERENCES PARTY(PartyId)
);

-- =====================================================
-- LOOKUP / REFERENCE TABLES
-- =====================================================

CREATE TABLE PRODUCT_TYPE (
    ProductTypeId INT PRIMARY KEY IDENTITY(1,1),
    ProductTypeName VARCHAR(100) NOT NULL
);

CREATE TABLE CONTRACT_STATUS (
    StatusId INT PRIMARY KEY IDENTITY(1,1),
    StatusName VARCHAR(100) NOT NULL
);

CREATE TABLE ACTIVITY_TYPE (
    ActivityTypeId INT PRIMARY KEY IDENTITY(1,1),
    ActivityTypeName VARCHAR(100) NOT NULL
);

CREATE TABLE DOCUMENT_TYPE (
    DocumentTypeId INT PRIMARY KEY IDENTITY(1,1),
    DocumentTypeName VARCHAR(100) NOT NULL
);

CREATE TABLE INTERACTION_MEDIUM (
    MediumId INT PRIMARY KEY IDENTITY(1,1),
    MediumName VARCHAR(100) NOT NULL
);

-- =====================================================
-- CORE BUSINESS TABLES
-- =====================================================

CREATE TABLE PRODUCT (
    ProductId INT PRIMARY KEY IDENTITY(1,1),
    ProductName VARCHAR(150) NOT NULL,
    ProductTypeId INT,
    FOREIGN KEY (ProductTypeId)
        REFERENCES PRODUCT_TYPE(ProductTypeId)
);

CREATE TABLE CONTRACT (
    ContractId INT PRIMARY KEY IDENTITY(1,1),
    ContractHolderId INT NOT NULL,
    ProductId INT NOT NULL,
    StartDate DATE,
    EndDate DATE,
    StatusId INT,
    FOREIGN KEY (ContractHolderId)
        REFERENCES CONTRACT_HOLDER(PartyId),
    FOREIGN KEY (ProductId)
        REFERENCES PRODUCT(ProductId),
    FOREIGN KEY (StatusId)
        REFERENCES CONTRACT_STATUS(StatusId)
);

CREATE TABLE ACTIVITY (
    ActivityId INT PRIMARY KEY IDENTITY(1,1),
    ContractId INT NOT NULL,
    ActivityTypeId INT,
    ActivityDate DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (ContractId)
        REFERENCES CONTRACT(ContractId),
    FOREIGN KEY (ActivityTypeId)
        REFERENCES ACTIVITY_TYPE(ActivityTypeId)
);

CREATE TABLE COMMISSION (
    CommissionId INT PRIMARY KEY IDENTITY(1,1),
    ContractId INT NOT NULL,
    FinancialProfessionalId INT,
    Amount DECIMAL(10,2),
    CommissionDate DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (ContractId)
        REFERENCES CONTRACT(ContractId),
    FOREIGN KEY (FinancialProfessionalId)
        REFERENCES FINANCIAL_PROFESSIONAL(PartyId)
);

CREATE TABLE DOCUMENT (
    DocumentId INT PRIMARY KEY IDENTITY(1,1),
    ActivityId INT NOT NULL,
    DocumentTypeId INT,
    CreatedDate DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (ActivityId)
        REFERENCES ACTIVITY(ActivityId),
    FOREIGN KEY (DocumentTypeId)
        REFERENCES DOCUMENT_TYPE(DocumentTypeId)
);

CREATE TABLE INTERACTION (
    InteractionId INT PRIMARY KEY IDENTITY(1,1),
    PartyId INT NOT NULL,
    MediumId INT,
    InteractionDate DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (PartyId)
        REFERENCES PARTY(PartyId),
    FOREIGN KEY (MediumId)
        REFERENCES INTERACTION_MEDIUM(MediumId)
);

-- =====================================================
-- DATA LAKE METADATA TABLES
-- =====================================================

CREATE TABLE DATA_SOURCE (
    DataSourceId INT PRIMARY KEY IDENTITY(1,1),
    SourceName VARCHAR(150),
    SourceType VARCHAR(100),
    ProviderName VARCHAR(150),
    Description VARCHAR(500)
);

CREATE TABLE RAW_DATASET (
    DatasetId INT PRIMARY KEY IDENTITY(1,1),
    DataSourceId INT NOT NULL,
    DatasetName VARCHAR(150),
    FileFormat VARCHAR(50),
    StoragePath VARCHAR(500),
    CollectionDate DATE,
    DataCategory VARCHAR(100),
    FOREIGN KEY (DataSourceId)
        REFERENCES DATA_SOURCE(DataSourceId)
);

-- =====================================================
-- PART 4 MACHINE LEARNING OUTPUT TABLE
-- =====================================================

CREATE TABLE RISK_ASSESSMENT (
    RiskAssessmentId INT PRIMARY KEY IDENTITY(1,1),

    PartyId INT,

    StateName VARCHAR(100),

    ObesityRate FLOAT,
    InactivityRate FLOAT,
    TobaccoRate FLOAT,

    RecommendedBusinessStrategy VARCHAR(100),

    PricingRecommendation VARCHAR(255),

    UnderwritingRecommendation VARCHAR(255),

    MarketSegment VARCHAR(150),

    ProductRecommendation VARCHAR(500),

    AssessmentDate DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (PartyId)
        REFERENCES PARTY(PartyId)
);

-- =====================================================
-- INDEXES FOR QUERY OPTIMIZATION
-- =====================================================

CREATE INDEX idx_contract_holder
ON CONTRACT(ContractHolderId);

CREATE INDEX idx_contract_product
ON CONTRACT(ProductId);

CREATE INDEX idx_activity_contract
ON ACTIVITY(ContractId);

CREATE INDEX idx_commission_contract
ON COMMISSION(ContractId);

CREATE INDEX idx_commission_professional
ON COMMISSION(FinancialProfessionalId);

CREATE INDEX idx_document_activity
ON DOCUMENT(ActivityId);

CREATE INDEX idx_interaction_party
ON INTERACTION(PartyId);

CREATE INDEX idx_raw_dataset_source
ON RAW_DATASET(DataSourceId);

CREATE INDEX idx_risk_party
ON RISK_ASSESSMENT(PartyId);

CREATE INDEX idx_risk_state
ON RISK_ASSESSMENT(StateName);

CREATE INDEX idx_risk_date
ON RISK_ASSESSMENT(AssessmentDate);

-- =====================================================
-- SAMPLE LOOKUP DATA
-- =====================================================

INSERT INTO PRODUCT_TYPE (ProductTypeName)
VALUES
('Health Insurance'),
('Life Insurance'),
('Wellness Plan');

INSERT INTO CONTRACT_STATUS (StatusName)
VALUES
('Pending'),
('Active'),
('Expired');

INSERT INTO ACTIVITY_TYPE (ActivityTypeName)
VALUES
('Quote Request'),
('Risk Assessment'),
('Policy Approval'),
('Document Generation');

INSERT INTO DOCUMENT_TYPE (DocumentTypeName)
VALUES
('Insurance Quote'),
('Policy Document'),
('Risk Assessment Report');

INSERT INTO INTERACTION_MEDIUM (MediumName)
VALUES
('Email'),
('Phone'),
('Web Portal');

-- =====================================================
-- END OF SCHEMA
-- =====================================================