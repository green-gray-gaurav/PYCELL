# PyCell Frontend

This is a minimal React + Vite frontend for a notebook-like UI (cells with versioning).

Features
- Create / load / rename / delete notebooks (stored in `localStorage`).
- Add / delete / edit cells.
- Each cell supports versions (create new version, select version, delete selected version).
- Save notebook: stores to `localStorage` and downloads a JSON file.

Quick start

1. Install dependencies:

```powershell
cd frontend
npm install
```

2. Run dev server:

```powershell
npm run dev
```

This will open the frontend at the Vite dev URL shown in the terminal.

Notes
- Notebooks are persisted to browser `localStorage` under the key `pycell_notebooks`.
- Saving a notebook will also download a JSON file for external backup.
