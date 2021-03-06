import React, { useState, useCallback, useEffect } from "react";
import { Row, Card, Col, Button, Modal, Table } from "react-bootstrap";
import { useGetAPI, usePutAPI } from '../useAPI'
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import axios from 'axios';
import PageTitle from "../../layouts/PageTitle";
// import ColorPicker from "./Color";
import ColorPicker_ from "material-ui-color-picker";
import { ToastContainer, toast } from 'react-toastify'

// import { Dropdown, Tab, Nav } from "react-bootstrap";
// import { Link } from "react-router-dom";
import useForm from 'react-hook-form';
import createPalette from "@material-ui/core/styles/createPalette";
function refreshPage() {
  window.location.reload(false);
}
const ActivityCreateModal = ({show, onShowShange, activityData}) => {
    const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])
    const activitiesEND = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/activite/`
    const activityCreateEND = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/activite/create`
    // const creneauPerAbonnementEND = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/`

const [name, setName] = useState('')
const [salle, setSalle] = useState('')
const [error, setError] = useState(false)
const [success, setSuccess] = useState(false)

const notifySuccess = () => {
  toast.success('Coach Creer Avec Succée', {
    position: 'top-right',
    autoClose: 5000,
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
  })
}
const notifyError = () => {
  toast.error('erreur lors de la création du Coach', {
    position: 'top-right',
    autoClose: 5000,
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
  })
}
useEffect(() => {
  if (error == true) {
    notifyError()
  }
}, [error]);
useEffect(() => {
  if (success == true) {
    notifySuccess()
  }
}, [success]);
    const handleSubmit = e => {
        e.preventDefault();
        const activityFormData = {
            name              : name,
            salle             : Number(salle),
        }
        console.log(" =================> new Creneau ", activityFormData);
         axios.post(activityCreateEND, activityFormData).then(res => {
            console.log('new message',res.data);
            setSuccess(true)
        }).catch( err => {
          setError(true)
          console.log('responsessssss', err)
        }
        )
        // } catch (error) {
        //   const res = await axios.post(activityCreateEND, activityFormData)
        //   console.log("les erreurs 43", error);
        //   console.log('new Erreur',res);

            // refreshPage()
            handleShow()


      }
return ( 
    <Modal  className="fade bd-example-modal-lg" size="xl"onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-black'>Creer une nouvelle Activité  </Modal.Title>
      <Button variant="" className="close" onClick={handleShow} >
          <span>&times;</span>
      </Button>
    </Modal.Header>
    <Modal.Body>
      <form onSubmit={handleSubmit}>
          <div className="form-group row">
              <label className="col-sm-3 col-form-label">Nom </label>
              <div className="col-sm-9">
                  <input type="text" value={name} className="form-control" placeholder="..." onChange={e => setName(e.target.value)}/>
              </div>
          </div>
          
          {/* <div className="form-group row">
              <label className="col-sm-3 col-form-label">Couleur </label>
              <div className="col-sm-9">
              <div className="row">
                <div className="col-xl-4 col-lg-6 mb-3">
                  <div className="example">
                    <input
                      type="color"
                      className="as_colorpicker form-control"
                      value={color}
                      onChange={(e, value) => setColor(e.target.value)}
                    />
                  </div>
                </div>
                
                
              </div>
              </div>
          </div> */}

       
          <div className="form-group row">
              <label className="col-sm-3 col-form-label">Salle </label>
              <div className="col-sm-9">
                  <Autocomplete
                      onChange={((event, value) =>  
                        {
                        setSalle(value.id)
                    }
                        )} 
                    //   value={salles}
                      options={activityData['salllesActivities']}
                      getOptionSelected={(option) =>  option['id']}

                      id="size-small-standard-multi"
                      getOptionLabel={(option) =>  ( option['name'])}
                      renderInput={(params) =>
                  (<TextField {...params} name="salle" label="salle" variant="outlined" fullWidth />)}
                />
              </div>
          </div>
          <div className="form-group row">
              <div className="col-sm-10">
                  <button type="submit" className="btn btn-primary">
                      Valider
                  </button>
              </div>
          </div>
      </form>
     </Modal.Body>

    </Modal>
)

}
export default ActivityCreateModal;