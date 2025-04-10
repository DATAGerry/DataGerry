export interface CmdbPerson {
    public_id?: number;
    display_name?: string; // Not directly editable, derived from first_name + last_name
    first_name: string;
    last_name: string;
    phone_number?: string;
    email?: string;
    groups?: number[]; // list of CmdbPersonGroup public_id
  }
  