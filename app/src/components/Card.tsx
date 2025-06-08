import React from "react";

interface CardProps {
  name: string;
  status: string;
  link?: string;
}

export default function Card({ name, status, link }: CardProps) {
  return (
    <div className="card outline border-white rounded-xl bg-black">
      <div className="container gap-4 flex flex-col px-8">
        <h4>
          <b>{name}</b>
        </h4>
        <p>{status}</p>
        {link && (
          <a
            href={link}
            target="_blank"
            rel="noopener noreferrer"
          >
            {link}
          </a>
        )}
      </div>
    </div>
  );
}