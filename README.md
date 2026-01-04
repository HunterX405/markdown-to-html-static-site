## 📄 Static Site Generator (Markdown to HTML) in Python

A simple **static site generator built in Python** that converts Markdown files into HTML pages.
This project was created as a **guided learning project from Boot.dev** to practice Python, file processing, and basic static site generation concepts.

The generated site is currently deployed to **GitHub Pages** (https://hunterx405.github.io/markdown-to-html-static-site/).

---

## ✨ Features

* Converts Markdown (`.md`) files into HTML
* Supports basic Markdown elements (headings, paragraphs, links, lists)
* Processes directories of content
* Outputs static HTML files ready for deployment
* Simple, dependency-light Python implementation

---

## 🛠 Tech Stack

* Python 3
* Standard Library (no heavy frameworks)
* GitHub Pages (for deployment)

---

## 🚀 Getting Started

### Prerequisites

* Python **3.10+** installed

---

### Clone the Repository

```bash
git clone https://github.com/HunterX405/markdown-to-html-static-site.git
cd markdown-to-html-static-site
```

---

### Run the Generator (using Python)

```bash
./main.sh
```

> This will generate static HTML files in the output directory (e.g. `public/` or `docs/` depending on your setup) and deploy to a localhost server.

---

## 🌍 Deployment

The generated HTML files can be deployed to **GitHub Pages**:

1. Generate the site locally
   
```bash
./build.sh
```

2. Commit the output directory
3. Configure GitHub Pages to serve from that directory

Example:

```
Settings → Pages → Source → /docs or /root
```

---

## 📚 Learning Context

This project was built as part of the **Boot.dev BackEnd Path - Build a Static Site Generator in Python Course** and focuses on:

* File I/O
* Parsing and transforming text
* Markdown to HTML nodes as python classes
* HTML nodes to html syntax functions
* Practical backend-style Python workflows

## 📄 License

This project is for learning purposes and is open for educational use.
