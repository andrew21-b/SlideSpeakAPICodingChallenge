import React from "react";

interface CardProps {
  task_id: string;
  task_status: string;
  task_result?: string;
}

export default function Card({ task_id, task_status, task_result }: CardProps) {
  return (
    <div className="card outline border-white rounded-xl bg-black">
      <div className="container gap-4 flex flex-col px-8">
        <h4>
          <b>{task_id}</b>
        </h4>
        <p>{task_status}</p>
        {task_result && (
          <a
            href={task_result}
            target="_blank"
            rel="noopener noreferrer"
          >
            View result
          </a>
        )}
      </div>
    </div>
  );
}