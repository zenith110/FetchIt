import logo from './logo.svg';
import './App.css';
import React, { useEffect, useState, useRef } from 'react';
import { Form, Container, Row, Col, DropdownButton, Dropdown } from 'react-bootstrap'
const App = (props) => {
  const [animal, setAnimal] = useState([])
  const [animalBreed, setAnimalBreed] = useState("");
  const [subSpecies, setSubspecies] = useState([])
  const [visble, setVisble] = useState(false);;
  const [selectedSubSpecies, setSelectedSubSpecies] = useState("");
  const [fileOption, setFileOption] = useState("");
  const [speciesSize, setSpeciesSize] = useState(0);
  const [alertTextError, setAlertTextError] = useState("");
  const [alertTextErrorStyle, setAlertTextErrorStyle] = useState(false);
  const [uploadSettings, setUploadSettings] = useState(false);
  const [seeSubBreed, setSeeSubBreed] = useState(false);
  const [ formData, setFormData ] = useState({ files: [] });
  const inputFileRef = useRef();
  // const url = "https://api.fetchit.dev"
  const url = "http://localhost:5000"
  let sub_species = []
  useEffect(() => {
    fetch(url + '/species/allspecies/')
      .then((response) => response.json())
      .then((data) => setAnimal(data))
      .catch((error) => console.log(error))

  }, [])

  const handleCheck = (e) => {
    sub_species = e.target.value.split(",");
    var first_element_species = sub_species.shift()
    setSpeciesSize(0)
    if (sub_species.length < 2) {
      setSpeciesSize(sub_species.length);
      setSubspecies("");
      setAnimalBreed(first_element_species);
      sub_species = []
      setVisble(false);
    }
    else if (sub_species.length > 2) {
      setAnimalBreed(first_element_species);
      setSpeciesSize(sub_species.length);
      setSubspecies(sub_species);
      setVisble(true);
    }

  }
  const subSpeciesCheck = (e) => {
    setSelectedSubSpecies(e.target.value.slice(2))
  }
  const fileCheck = (e) => {
    setFileOption(e.target.value)
  }
  const uploadHandler = (e) => {
    e.preventDefault()
    const data = new FormData();

    for (const file of formData.files) {
      console.log(file)
      data.append('files[]', file, file.name);
    }
    console.log(data)
    if (speciesSize <= 2) {
      setUploadSettings(true);
      setSeeSubBreed(false);
      fetch(url + "/upload/single/", {
        method: "POST",
        mode: 'no-cors',
        cache: "no-cache",
        headers: {
          "content_type": "multipart/form-data",
        },
        body: data
      })
    }
    else if (speciesSize > 2) {
      setUploadSettings(true);
      setSeeSubBreed(true);
    }
  }
  return (
    <div>
      <Container className="checkbox-container">
        <h4 className="checkbox-title">
          Welcome to fetchit! below is the following species and sub-breeds that we have available!
        </h4>
        <select onChange={handleCheck}>
          <option selected hidden />
          {
            Object.entries(animal).map((key, value) => (
              <option value={key}>{key[0]}</option>
            ))
          }
        </select>
        <div style={{ display: visble ? 'block' : 'none' }}>
          <h4 id="sub_species">Select the sub species!
            <select onChange={subSpeciesCheck}>
              <option selected hidden />
              {
                Object.entries(subSpecies).map((key, value, thing) => (
                  <option value={key}>{key.slice(1)}</option>
                ))
              }
            </select>
          </h4>
        </div>
        <div>
          <h4>Select file upload option:</h4>
          <select onClick={fileCheck}>
            <option selected hidden />
            <option value="single">Single files</option>
          </select>
        </div>
        <form onSubmit={uploadHandler}>
          <input type="file" onChange={e => setFormData({ ...formData, files: [ ...formData.files, ...e.target.files ] })}/>
          <button>Upload</button>
        </form>
        <div style={{ display: uploadSettings ? 'block' : 'none' }}>
          <p>Animal: {animalBreed}</p>
          <p>File option: {fileOption}</p>
          <p style={{ display: seeSubBreed ? 'block' : 'none' }}>Sub Breed: {selectedSubSpecies}</p>
        </div>
        <p style={{ display: alertTextErrorStyle ? 'block' : 'none' }}>{alertTextError}</p>
      </Container>

    </div>)
}

export default App;
