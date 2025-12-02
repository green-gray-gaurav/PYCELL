import React, { useState, useEffect } from 'react'
import NotebookList from './components/NotebookList'
import NotebookEditor from './components/NotebookEditor'
import * as api from './api'

const STORAGE_KEY = 'pycell_notebooks'

export default function App() {
  const [notebooks, setNotebooks] = useState([])
  const [current, setCurrent] = useState(null)
  const [celldata , setcelldata] = useState({})

  useEffect(() => {
    // load notebooks from backend
    get_notebooks()
  }
  
  , [])

  // useEffect(() => {
  //   // always keep a local cache for quick reloads
  //   localStorage.setItem(STORAGE_KEY, JSON.stringify(notebooks))
  // }, [notebooks])

    function get_notebooks(){
      fetch('http://127.0.0.1:5000/get_all_notebook_names', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        })
          .then((res) => res.json())
          .then((data) => {
            console.log(data)
            setNotebooks(data.notebook_names)
            setCurrent(data.notebook_names[0])
          })
          .catch((err) => {
            alert('Failed to load notebook names from backend;')
            console.log('get_all_notebook_names error', err)
          })
    }


  function createNotebook(name) {
    if (!name) return
    fetch('http://127.0.0.1:5000/create_notebook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ notebook_name: name }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data)
        get_notebooks()
      })
      .catch((err) => {
        alert('sdfdsf')
        console.log('create_notebook error', err)
      })
  }

  function deleteNotebook(name) {
    
  }

  function renameNotebook(oldName, newName) {
    if (!newName) return
    fetch('http://127.0.0.1:5000/rename_notebook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name_new: newName }),
    })
      .then((res) => res.json())
      .then(() => {
       
        setCurrent(newName)
      })
      .catch((err) => {
        alert('Failed to rename notebook in backend;')
        
      })
  }

  function saveNotebook(name, nb) {
    // prefer backend save
    fetch('http://127.0.0.1:5000/save_notebook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ notebook_name: name, notebook: nb }),
    })
      .then((res) => res.json())
      .then(() => {
        alert('Notebook saved successfully!')
      })
      .catch((err) => {
        alert('Failed to save notebook to backend;')
        
      })
  }

  function loadNotebook(name) {
    fetch('http://127.0.0.1:5000/load_notebook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ notebook_name: name }),
    })
      .then((res) => res.json())
      .then(() => {
        setCurrent(name)
      })
      .catch((err) => {
        alert('Failed to load notebook from backend;')
      })
  }

  return (
    <div className="app-root">
      <header>
        <h1>PyCell — Notebook Frontend</h1>
      </header>
      <div className="container">
        <NotebookList
          notebooks={notebooks}
          current={current}
          onCreate={createNotebook}
          onDelete={deleteNotebook}
          onRename={renameNotebook}
          onLoad={loadNotebook}
        />
        <main>
          {current != "" ? (
            <NotebookEditor
              notebook={current}
              onSave={(nb) => saveNotebook(current, nb)}
              onDelete={() => deleteNotebook(current)}
            />
          ) : (
            <div className="placeholder">Select or create a notebook</div>
          )}

        </main>
      </div>
    </div>
  )
}
