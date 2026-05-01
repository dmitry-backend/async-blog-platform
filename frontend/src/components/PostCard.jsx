import React from "react";
import styles from "./PostCard.module.css";
import { Link } from "react-router-dom";

const PostCard = ({ post }) => {
  return (
    <div className={styles.postCard}>
      <h3>{post.title}</h3>
      <p>{post.content}</p>
      <Link to={`/posts/${post.id}`}>Read more</Link>
    </div>
  );
};

export default PostCard;
