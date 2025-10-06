export interface Field {
  id: number;
  label: string;
  field_type: "text" | "number" | "date" | "dropdown" | "checkbox" | "file";
  required: boolean;
  options?: string[] | null;
}

export interface Form {
  id: number;
  name: string;
  description?: string;
  fields: Field[];
}

export interface ResponseData {
  field: number;
  value?: string | number | boolean | null;
  file?: File | null;
}
