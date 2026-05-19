import { useState, useEffect } from "react";
import api from "../api";
import "./TodoPage.css"

function TodoPage({ token, onLogout }) {
    // Quản lý dữ liệu ToDo
    const [todos, setTodos] = useState([]); // Mảng chứa danh sách các task từ Django gửi về
    const [newTodo, setNewTodo] = useState(""); // Lưu chữ người dùng đang gõ ở ô input
    const [filter, setFilter] = useState("all"); // Trạng thái bộ lọc: all/completed pending

    // Xử lý side effect: Bất cứ khi nào token thay đổi (vừa đăng nhập/đăng xuất) HOẶC người dùng bấm đổi bộ lọc (Tất cả -> Chưa xong) chạy lại hàm này
    useEffect(() => {
        fetchTodos();
    }, [filter]);

      // --- TODO CRUD ---
    const fetchTodos = async () => {
        try {
        const statusParam = filter !== "all" ? `?status=${filter}` : "";
        const res = await api.get(`todos/${statusParam}`);
        setTodos(res.data);
        } catch (error) {
        console.log(error);
        }
    };

    const createTodo = async (e) => {
        e.preventDefault();
        if (!newTodo) return;
        await api.post("todos/", { title: newTodo });
        setNewTodo("");
        fetchTodos();
    };

    const toggleComplete = async (todo) => {
        await api.put(`todos/${todo.id}/`, {
        ...todo,
        completed: !todo.completed,
        });
        fetchTodos();
    };

    const deleteTodo = async (id) => {
        await api.delete(`todos/${id}/`);
        fetchTodos();
    };

return (
  <>
    <meta charSet="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      {/* Google Fonts */}
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
      <link
        href="https://fonts.googleapis.com/css2?family=Bungee&family=Inter:wght@400&display=swap"
        rel="stylesheet"
    />
  <button className="logout" onClick={onLogout} style={{ float: "right", marginBottom: "20px" }}>Đăng xuất</button>
    <div style={{ maxWidth: "500px", margin: "50px auto", textAlign: "center" }}>
      <h2 className="todo-title">My Todo List</h2>
      
      {/* Form thêm task */}
      <form className="todo-input-group" onSubmit={createTodo}> 
        <input 
          className="todo-input" type="text" value={newTodo} onChange={(e) => setNewTodo(e.target.value)} 
          placeholder="Thêm việc cần làm..." style={{ width: "70%", padding: "8px" }} 
        />
        <button className="add-button" type="submit" style={{ padding: "8px" }}>Thêm</button>
      </form>

      {/* Filter Options */}
      <div className="filter-group" style={{ margin: "20px 0" }}>
        <button className="filter-button" onClick={() => setFilter("all")} disabled={filter === "all"}>Tất cả</button>
        <button className="filter-button" onClick={() => setFilter("completed")} disabled={filter === "completed"}>Hoàn thành</button>
        <button className="filter-button" onClick={() => setFilter("pending")} disabled={filter === "pending"}>Chưa xong</button>
      </div>

      {/* Danh sách Task */}
      <ul className="task-list" style={{ listStyle: "none", padding: 0 }}>
        {todos.map((todo) => (
          <li className="list" key={todo.id} style={{ display: "flex", justifyContent: "space-between", padding: "10px", borderBottom: "3px solid #303030" }}>
            <span 
              onClick={() => toggleComplete(todo)} 
              style={{ textDecoration: todo.completed ? "line-through" : "none", cursor: "pointer", color: todo.completed ? "gray" : "black" }}
            >
              {todo.title}
            </span>
            <button className="delete" onClick={() => deleteTodo(todo.id)} style={{ color: "red", border: "none", background: "none", cursor: "pointer" }}>Xóa</button>
          </li>
        ))}
      </ul>
    </div>
    </>
  );
}

export default TodoPage;