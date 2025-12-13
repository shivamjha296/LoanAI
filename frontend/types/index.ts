// Application State Types
export interface ApplicationState {
    customer_name: string;
    customer_id: string;
    customer_phone?: string;
    customer_email?: string;
    customer_city?: string;
    customer_salary?: number;
    customer_occupation?: string;
    customer_employer?: string;
    customer_pan?: string;
    customer_bank?: string;
    customer_account?: string;
    
    pre_approved_limit?: number;
    credit_score?: number;
    current_offer?: any;
    
    application_status: string;
    application_initiated?: boolean;
    kyc_verified: boolean;
    kyc_data?: any;
    
    eligibility_evaluation?: any;
    loan_approved?: boolean;
    loan_application?: {
        application_id: string;
        customer_id: string;
        customer_name: string;
        loan_amount: number;
        tenure_months: number;
        purpose: string;
        application_date: string;
        status: string;
    };
    
    sanction_letter?: {
        sanction_reference: string;
        customer_name: string;
        loan_amount: number;
        interest_rate: number;
        tenure_months: number;
        emi_amount: number;
        generated_date: string;
        [key: string]: any;
    };
    
    interaction_history?: Array<{
        action: string;
        timestamp: string;
        [key: string]: any;
    }>;
    
    offer_shown?: boolean;
}

// Message Types
export interface Message {
    id: string;
    role: 'user' | 'assistant' | 'system';
    content: string;
    timestamp: Date;
}

// Customer Types
export interface Customer {
    id: string;
    name: string;
    city: string;
    monthly_salary: number;
    credit_score: number;
    pre_approved_limit: number;
}

// API Response Types
export interface ApiResponse<T = any> {
    status: string;
    data?: T;
    message?: string;
    error?: string;
}
