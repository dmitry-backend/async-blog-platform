import React, { useState, useContext } from "react";
import styles from "./CreatePost.module.css";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext"; // NEW: to get JWT token

const CreatePost = () => {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  const navigate = useNavigate(); // NEW: redirect after success
  const { user } = useContext(AuthContext); // NEW: access auth state (token assumed inside user)

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // NEW: API request to backend
      const response = await fetch("http://localhost:8000/posts/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",

          // NEW: JWT authentication (based on your backend)
          Authorization: `Bearer ${user?.token}`,
        },
        body: JSON.stringify({
          title,
          content,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to create post");
      }

      const data = await response.json(); // NEW: backend response

      console.log("Created post:", data);

      // NEW: reset form
      setTitle("");
      setContent("");

      // NEW: redirect to home after success
      navigate("/");

    } catch (error) {
      console.error("Error creating post:", error);
    }
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>Create Post</h2>

      <form className={styles.form} onSubmit={handleSubmit}>

        <input
          className={styles.input}
          type="text"
          placeholder="Post title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <textarea
          className={styles.textarea}
          placeholder="Post content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          rows="6"
        />

        <button className={styles.button} type="submit">
          CREATE
        </button>

      </form>
    </div>
  );
};

export default CreatePost;
