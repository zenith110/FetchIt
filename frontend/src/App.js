import logo from './logo.svg';
import './App.css';
import React, { useEffect, useState, useRef } from 'react';
import { Form, Container, Row, Col, DropdownButton, Dropdown } from 'react-bootstrap'
const App = (props) => {
  const [animal, setAnimal] = useState([])
  const [animalBreed, setAnimalBreed] = useState("");
  const [subSpecies, setSubspecies] = useState([]);
  const [visble, setVisble] = useState(false);
  const [selectedSubSpecies, setSelectedSubSpecies] = useState("");
  const [fileOption, setFileOption] = useState("");
  const [speciesSize, setSpeciesSize] = useState(0);
  const [uploadSettings, setUploadSettings] = useState(false);
  const [seeSubBreed, setSeeSubBreed] = useState(false);
  const [ formData, setFormData ] = useState({ files: [] });
  const [singleVisble, setSingleVisble] = useState(false);
  const [multiVisble, setMultiVisble] = useState(false);
  const url = "https://api.fetchit.dev"
  // Enable for localhost development
  // const url = "http://localhost:5000"
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
    if(e.target.value === "single"){
      setSingleVisble(true);
      setMultiVisble(false);
    }
    else if(e.target.value === "multi"){
      setSingleVisble(false);
      setMultiVisble(true);
    }
    setFileOption(e.target.value)
  }
  function multiUpload(uploadBoolSettings, subBoolBreed, message, data){
    setUploadSettings(uploadBoolSettings);
      setSeeSubBreed(subBoolBreed);
      fetch(url + "/upload/multi/", {
        method: "POST",
        mode: 'no-cors',
        cache: "no-cache",
        headers:{
          contentType: "multipart/form-data",
        },
        body: data
      }).then(alert(message))
  }

  function singleUpload(uploadBoolSettings, subBoolBreed, message, data){
    setUploadSettings(uploadBoolSettings);
      setSeeSubBreed(subBoolBreed);
      fetch(url + "/upload/single/", {
        method: "POST",
        mode: 'no-cors',
        cache: "no-cache",
        headers:{
          contentType: "multipart/form-data",
        },
        body: data
      }).then(alert(message))
  }
  const uploadHandler = (e) => {
    const data = new FormData();
    
    for (const file of formData.files) {
      data.append('animal', animalBreed)
      data.append('files[]', file, file.name);
      data.append("sub_species", selectedSubSpecies)
    }
  //   for (var pair of data) {
  //     console.log(pair); 
  // }
    if (speciesSize <= 2) {
      if(fileOption === "single")
        singleUpload(true, false, "Thank you for your submission, it has been sent!", data)
      else if(fileOption === "multi")
        multiUpload(true, false, "Thank you for your submission, it has been sent!", data)
    }
    else if (speciesSize > 2) {
      if(fileOption === "single")
        singleUpload(true, true, "Thank you for your submission with sub species, it has been sent!", data)
      else if(fileOption === "multi")
        multiUpload(true, true, "Thank you for your submission with sub species, it has been sent!", data)
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
            <option value="multi">Multiple files</option>
          </select>
        </div>
        <form onSubmit={uploadHandler}>
          <input type="file" style = {{ display: singleVisble ? 'block' : 'none' }} accept=".png, .jpg" onChange={e => setFormData({ ...formData, files: [ ...formData.files, ...e.target.files ] })}/>
          <input type="file" multiple style = {{ display: multiVisble ? 'block' : 'none' }} accept=".png, .jpg" onChange={e => setFormData({ ...formData, files: [ ...formData.files, ...e.target.files ] })}/>
          <button>Upload</button>
        </form>
        <div style={{ display: uploadSettings ? 'block' : 'none' }}>
          <p>Animal: {animalBreed}</p>
          <p>File option: {fileOption}</p>
          <p style={{ display: seeSubBreed ? 'block' : 'none' }}>Sub Breed: {selectedSubSpecies}</p>
        </div>
      </Container>

    </div>)
}

export default App;
