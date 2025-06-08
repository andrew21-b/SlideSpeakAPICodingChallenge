"use client";
import Card from "@/components/Card";
import ImageUploadBox from "@/components/ImageUploadBox";
import Image from "next/image";
import { useState, useEffect } from "react";

type CardData = {
  task_id: string;
  task_status: string;
  task_result?: string;
};

export default function Home() {
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [cards, setCards] = useState<CardData[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchCards = async (): Promise<CardData[]> => {
    const res = await fetch("http://localhost/get_queue");
    const data = await res.json();
    console.log("API response:", data);
    return data.jobs || [];
  };

  useEffect(() => {
    fetchCards()
      .then(setCards)
      .catch((error) => {
        alert("Error fetching cards: " + error);
        setCards([]);
      });
  }, []);

  const handleImageChange = (file: File | null) => {
    setImageFile(file);
    setPreviewUrl(file ? URL.createObjectURL(file) : null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!imageFile) return alert("Please upload an image first.");
    setLoading(true);

    const formData = new FormData();
    formData.append("image", imageFile);

    const res = await fetch("http://localhost/geneterate_presentation", {
      method: "POST",
      body: formData,
    });

    setLoading(false);

    if (res.ok) {
      alert("Image uploaded successfully!");
      fetchCards().then(setCards);
    } else {
      alert("Upload failed.");
    }
  };
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <div className="flex gap-x-6 justify-start p-5 outline-offset-4 rounded-xl border-2 border-dashed border-gray-400 bg-zinc-700">
        {cards.map((card, idx) => (
          <Card
            key={card.task_id || idx}
            task_id={card.task_id || "No task_id"}
            task_status={card.task_status || "No task_status"}
            task_result={card.task_result || ""}
          />
        ))}
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
            disabled={loading}
          />
          <button
            type="submit"
            disabled={!imageFile || loading}
            className={`rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:w-auto
              ${(!imageFile || loading) ? "opacity-50 cursor-not-allowed" : ""}`}
          >
            <Image
              className="dark:invert"
              src="/vercel.svg"
              alt="Vercel logomark"
              width={20}
              height={20}
            />
            {loading ? "Uploading..." : "Submit"}
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
