import logo from './logo.svg';
import './App.css';
import React, {useEffect, useState} from 'react';
import {Form, Container, Row, Col, DropdownButton, Dropdown} from 'react-bootstrap'
const App = (props) => {
  const [animal, setAnimal] = useState([])
    //const [checkedSubs, setCheckedSubs] = useState([])

    const url = "https://api.fetchit.dev"
    
    useEffect(()=>{
        fetch(url + '/species/allspecies/')
        .then ((response) => response.json())
        .then((data) => setAnimal(data))
        .catch((error) => console.log(error))

    }, [])
    const handleCheck = (e) =>
    {
        console.log(e)
        if(e.target.checked == true)
        {
                props.setCheckedSubs([...props.checkedSubs, e.target.id])
                console.log("now selected ", e)

        }
        else if (e.target.checked == false)
        {
            props.setCheckedSubs(props.checkedSubs.filter(sub => sub != e.target.id))

        }

        


    }
  
  return(<div>
    <Container className="checkbox-container">
        <h4 className="checkbox-title">
            Choose! We tell you when your sub is on sale
        </h4>
        <select value={handleCheck}>
        {
          Object.keys(animal).map((key, index) => ( 
            <option value={key}>{key}</option>
          ))
          
        }
        
        </select>
    </Container>

</div>)
}

export default App;
