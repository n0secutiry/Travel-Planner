from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from models import SessionLocal, engine
from utils import fetch_place_data

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/projects/", response_model=schemas.Project)
async def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = models.Project(
        name=project.name, description=project.description, start_date=project.start_date)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)


    if project.places:
        if len(project.places) > 10:
            raise HTTPException(
                status_code=400, detail="Maximum 10 places per project")
        for place_data in project.places:
            place = db.query(models.Place).filter(
                models.Place.external_id == place_data.external_id).first()
            if not place:
                place = models.Place(
                    external_id=place_data.external_id, title=place_data.title)
                db.add(place)
                db.commit()
                db.refresh(place)
            project_place = models.ProjectPlace(
                project_id=db_project.id, place_id=place.id)
            db.add(project_place)
        db.commit()
    return db_project


@app.get("/projects/", response_model=List[schemas.Project])
def list_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()


@app.get("/projects/{project_id}", response_model=schemas.Project)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(
        models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.put("/projects/{project_id}", response_model=schemas.Project)
def update_project(project_id: int, project_update: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(
        models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in project_update.dict(exclude_unset=True).items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project


@app.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(
        models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    visited_places = db.query(models.ProjectPlace).filter(
        models.ProjectPlace.project_id == project_id,
        models.ProjectPlace.visited == True
    ).first()
    if visited_places:
        raise HTTPException(
            status_code=400, detail="Cannot delete project with visited places")
    db.delete(project)
    db.commit()
    return {"ok": True}


@app.post("/projects/{project_id}/places/", response_model=schemas.ProjectPlace)
async def add_place_to_project(project_id: int, place_data: schemas.ProjectPlaceCreate, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(
        models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    current_places_count = db.query(models.ProjectPlace).filter(
        models.ProjectPlace.project_id == project_id).count()
    if current_places_count >= 10:
        raise HTTPException(
            status_code=400, detail="Maximum 10 places per project")


    try:
        place_info = await fetch_place_data(place_data.place_external_id)
    except HTTPException as e:
        raise e  


    place = db.query(models.Place).filter(
        models.Place.external_id == place_data.place_external_id).first()
    if not place:
        place = models.Place(
            external_id=place_info["external_id"],
            title=place_info["title"],
            api_data=str(place_info["api_data"])  
        )
        db.add(place)
        db.commit()
        db.refresh(place)


    existing = db.query(models.ProjectPlace).filter(
        models.ProjectPlace.project_id == project_id,
        models.ProjectPlace.place_id == place.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Place already in project")


    project_place = models.ProjectPlace(
        project_id=project_id,
        place_id=place.id,
        notes=place_data.notes,
        visited=place_data.visited
    )
    db.add(project_place)
    db.commit()
    db.refresh(project_place)
    return project_place


@app.put("/projects/{project_id}/places/{place_id}", response_model=schemas.ProjectPlace)
def update_project_place(project_id: int, place_id: int, update_data: schemas.ProjectPlaceBase, db: Session = Depends(get_db)):
    project_place = db.query(models.ProjectPlace).filter(
        models.ProjectPlace.project_id == project_id,
        models.ProjectPlace.place_id == place_id
    ).first()
    if not project_place:
        raise HTTPException(
            status_code=404, detail="Place not found in this project")
    if update_data.notes is not None:
        project_place.notes = update_data.notes
    if update_data.visited is not None:
        project_place.visited = update_data.visited
    db.commit()
    db.refresh(project_place)
    return project_place


@app.get("/projects/{project_id}/places/", response_model=List[schemas.ProjectPlace])
def list_project_places(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(
        models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project.project_places


@app.get("/projects/{project_id}/places/{place_id}", response_model=schemas.ProjectPlace)
def get_project_place(project_id: int, place_id: int, db: Session = Depends(get_db)):
    project_place = db.query(models.ProjectPlace).filter(
        models.ProjectPlace.project_id == project_id,
        models.ProjectPlace.place_id == place_id
    ).first()
    if not project_place:
        raise HTTPException(
            status_code=404, detail="Place not found in this project")
    return project_place
