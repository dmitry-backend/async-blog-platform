import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../api";
import styles from "./PostDetail.module.css";

const PostDetail = () => {
  const { id } = useParams();
  const [post, setPost] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const loadPost = async () => {
      setLoading(true);
      setError("");

      try {
        const response = await api.fetchPostById(id);
        if (!response.success) {
          setError(response.error || "Failed to load post");
          return;
        }
        setPost(response.data);
      } catch (err) {
        setError(
          err.message || "An unexpected error occurred while loading the post"
        );
      } finally {
        setLoading(false);
      }
    };

    loadPost();
  }, [id]);

  if (loading) return <p>Loading post details...</p>;
  if (error) return <p className={styles.error}>{error}</p>;
  if (!post) return null;

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>{post.title}</h2>
      <p className={styles.content}>{post.content}</p>
    </div>
  );
};

export default PostDetail;
