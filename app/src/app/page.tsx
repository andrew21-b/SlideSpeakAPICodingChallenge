"use client";
import Card from "@/components/Card";
import ImageUploadBox from "@/components/ImageUploadBox";
import Image from "next/image";
import { useState } from "react";

export default function Home() {
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handleImageChange = (file: File | null) => {
    setImageFile(file);
    setPreviewUrl(file ? URL.createObjectURL(file) : null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!imageFile) return alert("Please upload an image first.");

    const formData = new FormData();
    formData.append("image", imageFile);

    const res = await fetch("/submit", {
      method: "POST",
      body: formData,
    });

    if (res.ok) {
      alert("Image uploaded successfully!");
    } else {
      alert("Upload failed.");
    }
  };
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <div className="flex gap-x-6 justify-start p-5 outline-offset-4 rounded-xl border-2 border-dashed border-gray-400 bg-zinc-700">
        <Card
          name="John Doe"
          status="Architect & Engineer"
          link="https://www.google.com/webhp?hl=en&sa=X&ved=0ahUKEwj7pquL2uCNAxW2QUEAHb3aGTgQPAgI"
        />
      </div>
      <main className="flex flex-col gap-[32px] items-center">
        <h1 className="text-4xl sm:text-5xl font-bold text-center sm:text-left">
          SlideSpeak API Coding Challenge
        </h1>

        <form
          onSubmit={handleSubmit}
          className="flex flex-col items-center gap-4 w-full"
        >
          <ImageUploadBox
            onImageChange={handleImageChange}
            previewUrl={previewUrl}
          />
          <button
            type="submit"
            className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:w-auto"
          >
            <Image
              className="dark:invert"
              src="/vercel.svg"
              alt="Vercel logomark"
              width={20}
              height={20}
            />
            Submit
          </button>
        </form>
      </main>
      <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center">
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://github.com/andrew21-b/SlideSpeakAPICodingChallenge"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="/globe.svg"
            alt="Globe icon"
            width={16}
            height={16}
          />
          Go to repository →
        </a>
      </footer>
    </div>
  );
}
