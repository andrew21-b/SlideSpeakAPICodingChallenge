import { useRef } from "react";

interface ImageUploadBoxProps {
  onImageChange: (file: File | null) => void;
  previewUrl: string | null;
  disabled?: boolean;
}

export default function ImageUploadBox({
  onImageChange,
  previewUrl,
  disabled,
}: ImageUploadBoxProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  return (
    <div className="flex flex-col items-center gap-4 p-6 rounded-xl border-2 border-dashed border-gray-400 bg-zinc-700">
      <label className="cursor-pointer text-white">
        <span className="block mb-2 font-semibold">Upload an image</span>
        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          onChange={(e) => {
            if (!disabled && e.target.files && e.target.files[0]) {
              onImageChange(e.target.files[0]);
            }
          }}
          className="hidden"
          disabled={disabled}
        />
        <span
          className={`inline-block px-4 py-2 bg-blue-600 rounded text-white hover:bg-blue-500 mt-2 ${
            disabled ? "opacity-50 cursor-not-allowed" : ""
          }`}
        >
          Choose an image
        </span>
      </label>
      {previewUrl && (
        <img
          src={previewUrl}
          alt="Preview"
          className="mt-4 max-w-xs max-h-48 rounded shadow"
        />
      )}
    </div>
  );
}
