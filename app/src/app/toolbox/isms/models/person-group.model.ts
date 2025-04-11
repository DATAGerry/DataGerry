export interface CmdbPersonGroup {
    public_id?: number;
    name: string;
    email?: string;
    group_members?: number[]; // list of CmdbPerson public_id
  }
