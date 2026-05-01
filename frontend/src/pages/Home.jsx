import React, { useEffect, useState } from "react";
import PostCard from "../components/PostCard";
import { fetchPosts } from "../api/posts";
import styles from "./Home.module.css";

const Home = () => {
  const [posts, setPosts] = useState([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const loadPosts = async () => {
      setLoading(true);
      setErrorMessage("");

      try {
        const response = await fetchPosts({ page, size: 10 });

        // Handle the response correctly
        const postsData = response?.data || response || [];
        setPosts(Array.isArray(postsData) ? postsData : []);

      } catch (err) {
        console.error(err);
        setErrorMessage(err.message || "Failed to load posts");
        setPosts([]);
      } finally {
        setLoading(false);
      }
    };

    loadPosts();
  }, [page]);

  return (
    <main className={styles.container}>
      <h2 className={styles.title}>All Posts</h2>

      {loading && <p>Loading posts...</p>}
      {errorMessage && <p className={styles.error}>{errorMessage}</p>}

      {!loading && !errorMessage && (
        <div className={styles.postsWrapper}>
          {posts.map((post) => (
            <PostCard key={post.id} post={post} />
          ))}
        </div>
      )}

      {!loading && posts.length === 0 && !errorMessage && (
        <p>No posts found.</p>
      )}

      <div className={styles.pagination}>
        <button
          onClick={() => setPage((p) => Math.max(p - 1, 1))}
          disabled={page === 1}
        >
          Previous
        </button>
        <span>Page {page}</span>
        <button
          onClick={() => setPage((p) => p + 1)}
          disabled={posts.length < 10}
        >
          Next
        </button>
      </div>
    </main>
  );
};

export default Home;
