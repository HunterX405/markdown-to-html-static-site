## 📄 Static Site Generator (Markdown to HTML) in Python

A **Python-based static site generator** that converts Markdown content into HTML pages using **Jinja2 templates** and modern Python practices.
This project was originally built as a guided project from **Boot.dev** and later extended with cleaner architecture, improved tooling, and maintainable design patterns.

**Live Demo Site:** https://hunterx405.github.io/markdown-to-html-static-site/

---

## ✨ Features

* Converts Markdown files into static HTML pages
* Uses **Jinja2** for templated page rendering
* Fully based on **`pathlib.Path`** for object-oriented file handling
* Uses **`@dataclass`** to model HTML nodes and site structure
* Clean separation between content, templates, and build logic
* Supports static assets (images, CSS)
* Output ready for **GitHub Pages** or any static hosting

---

## 🧰 Tech Stack

* **Python 3.10+**
* `pathlib.Path`
* `dataclasses`
* **Jinja2**
* **uv** (project & dependency manager)
* Markdown → HTML conversion
* Shell scripts for build automation

---

## 📁 Project Structure

```text
.
├── content/                  # Markdown source content
├── docs/                     # Generated static site output
├── src/                      # Core application logic
│   ├── generate.py           # Site generation logic
│   ├── htmlnode.py           # HTML node abstractions
│   ├── md_to_html.py         # Markdown → HTML conversion
│   ├── main.py               # Application entry point
│   ├── test_htmlnode.py
│   └── test_md_to_html.py
├── static/                   # Static assets (copied to output)
├── templates/                # Jinja2 HTML templates
├── build.sh                  # Build script
├── main.sh                   # Run script
├── test.sh                   # Test runner
├── pyproject.toml            # uv project configuration
├── uv.lock
├── README.md
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

* **Python 3.12+**
* **uv** installed

  ```bash
  pip install uv
  ```

---

### Clone the Repository

```bash
git clone https://github.com/HunterX405/markdown-to-html-static-site.git
cd markdown-to-html-static-site
```

---

### Install Dependencies

```bash
uv sync
```

---

### Build the Site

```bash
./build.sh
```

The generated static site will be written to the `docs/` directory.

---

### Run Tests

```bash
./test.sh
```

### Build and Run the Site Locally

```bash
./main.sh
```

---

## 🌍 Deployment

The contents of the `docs/` directory are ready for deployment via **GitHub Pages**:

1. Generate the site
2. Commit the `docs/` folder
3. Configure GitHub Pages to serve from `/docs`

---

## 🧠 Design Highlights

* **Pathlib-first design** for safer and clearer file operations
* **Dataclass-based HTML node system** for structured rendering
* Template-driven HTML generation via **Jinja2**
* Clear separation of:

  * Content (`content/`)
  * Logic (`src/`)
  * Output (`docs/`)
  * Assets (`static/`)

---

## 📚 Learning Context

Built as part of the **Boot.dev Backend Track**, then independently refined to follow modern Python engineering best practices.

---

## 📄 License

This project is intended for educational and portfolio use.
