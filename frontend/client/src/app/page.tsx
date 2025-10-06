"use client";
import { useEffect, useState, FormEvent, ChangeEvent } from "react";
import api from "../lib/api";
import { Form as FormType, Field } from "../types/form";

export default function HomePage() {
  const [forms, setForms] = useState<FormType[]>([]);
  const [selectedForm, setSelectedForm] = useState<FormType | null>(null);
  const [responses, setResponses] = useState<
    Record<number, string | boolean | File | null>
  >({});
  const [clientName, setClientName] = useState<string>("");
  const [clientEmail, setClientEmail] = useState<string>("");

  // Fetch forms
  useEffect(() => {
    api
      .get<FormType[]>("/forms/")
      .then((res) => setForms(res.data))
      .catch((err) => console.error("Error fetching forms:", err));
  }, []);

  const handleChange = (
    fieldId: number,
    value: string | boolean | File | null
  ) => {
    setResponses((prev) => ({ ...prev, [fieldId]: value }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!selectedForm) return;

    const payload = new FormData();
    payload.append("form", selectedForm.id.toString());
    payload.append("client_name", clientName);
    payload.append("client_email", clientEmail);

    selectedForm.fields.forEach((field) => {
      const value = responses[field.id];
      const prefix = `responses[${field.id}]`;

      if (field.field_type === "file" && value instanceof File) {
        payload.append(`${prefix}.file`, value);
      } else {
        payload.append(`${prefix}.field`, field.id.toString());
        payload.append(`${prefix}.value`, value?.toString() || "");
      }
    });

    try {
      const res = await api.post("/submit/", payload, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("✅ Form submitted successfully!");
      console.log(res.data);
      // reset form
      setClientName("");
      setClientEmail("");
      setResponses({});
      setSelectedForm(null);
    } catch (err) {
      console.error(err);
      alert("❌ Error submitting form.");
    }
  };

  // Step 4: UI
  if (!selectedForm) {
    return (
      <main className="p-6">
        <h1 className="text-xl font-bold mb-4">Available Forms</h1>
        <ul>
          {forms.map((form) => (
            <li key={form.id}>
              <button
                onClick={() => setSelectedForm(form)}
                className="text-blue-600 underline"
              >
                {form.name}
              </button>
            </li>
          ))}
        </ul>
      </main>
    );
  }

  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold mb-4">{selectedForm.name}</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Client info */}
        <div>
          <label className="block font-medium mb-1">Your Name</label>
          <input
            type="text"
            value={clientName}
            onChange={(e) => setClientName(e.target.value)}
            required
            className="border p-2 w-full"
            placeholder="Enter your name"
          />
        </div>

        <div>
          <label className="block font-medium mb-1">Your Email</label>
          <input
            type="email"
            value={clientEmail}
            onChange={(e) => setClientEmail(e.target.value)}
            required
            className="border p-2 w-full"
            placeholder="Enter your email"
          />
        </div>

        {/* Dynamic form fields */}
        {selectedForm.fields.map((field: Field) => (
          <div key={field.id} className="mb-4">
            <label className="block font-medium mb-1">{field.label}</label>

            {field.field_type === "text" && (
              <input
                type="text"
                onChange={(e: ChangeEvent<HTMLInputElement>) =>
                  handleChange(field.id, e.target.value)
                }
                className="border p-2 w-full"
              />
            )}

            {field.field_type === "number" && (
              <input
                type="number"
                onChange={(e: ChangeEvent<HTMLInputElement>) =>
                  handleChange(field.id, e.target.value)
                }
                className="border p-2 w-full"
              />
            )}

            {field.field_type === "date" && (
              <input
                type="date"
                onChange={(e: ChangeEvent<HTMLInputElement>) =>
                  handleChange(field.id, e.target.value)
                }
                className="border p-2 w-full"
              />
            )}

            {field.field_type === "dropdown" && (
              <select
                onChange={(e: ChangeEvent<HTMLSelectElement>) =>
                  handleChange(field.id, e.target.value)
                }
                className="border p-2 w-full"
              >
                <option value="">Select...</option>
                {field.options?.map((opt, idx) => (
                  <option key={idx} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
            )}

            {field.field_type === "checkbox" && (
              <input
                type="checkbox"
                onChange={(e: ChangeEvent<HTMLInputElement>) =>
                  handleChange(field.id, e.target.checked)
                }
              />
            )}

            {field.field_type === "file" && (
              <input
                type="file"
                onChange={(e: ChangeEvent<HTMLInputElement>) =>
                  handleChange(field.id, e.target.files?.[0] || null)
                }
              />
            )}
          </div>
        ))}

        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Submit
        </button>
      </form>
    </main>
  );
}
