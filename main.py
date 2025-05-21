from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Configuration base de données (adapter l'URL à votre MySQL ou PostgreSQL)
DATABASE_URL = "sqlite:///./produits.db"  # Remplacer par MySQL/Pg si besoin
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ProduitDB(Base):
    __tablename__ = "produits"
    numProduit = Column(Integer, primary_key=True, index=True)
    design = Column(String, index=True)
    prix = Column(Float)
    quantite = Column(Integer)

Base.metadata.create_all(bind=engine)

class Produit(BaseModel):
    numProduit: int
    design: str
    prix: float
    quantite: int
    class Config:
        orm_mode = True

class ProduitUpdate(BaseModel):
    design: Optional[str] = None
    prix: Optional[float] = None
    quantite: Optional[int] = None
    class Config:
        orm_mode = True

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/produits", response_model=Produit)
def ajouter_produit(produit: Produit, db: Session = Depends(get_db)):
    db_produit = db.query(ProduitDB).filter(ProduitDB.numProduit == produit.numProduit).first()
    if db_produit:
        raise HTTPException(status_code=400, detail="Produit existe déjà")
    db_produit = ProduitDB(**produit.dict())
    db.add(db_produit)
    db.commit()
    db.refresh(db_produit)
    return db_produit

@app.get("/produits", response_model=List[Produit])
def lister_produits(db: Session = Depends(get_db)):
    return db.query(ProduitDB).all()

@app.put("/produits/{num_produit}", response_model=Produit)
def modifier_produit(num_produit: int, produit: ProduitUpdate, db: Session = Depends(get_db)):
    db_produit = db.query(ProduitDB).filter(ProduitDB.numProduit == num_produit).first()
    if not db_produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    if produit.design is not None:
        db_produit.design = produit.design
    if produit.prix is not None:
        db_produit.prix = produit.prix
    if produit.quantite is not None:
        db_produit.quantite = produit.quantite
    db.commit()
    db.refresh(db_produit)
    return db_produit

@app.delete("/produits/{num_produit}")
def supprimer_produit(num_produit: int, db: Session = Depends(get_db)):
    db_produit = db.query(ProduitDB).filter(ProduitDB.numProduit == num_produit).first()
    if not db_produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    db.delete(db_produit)
    db.commit()
    return {"detail": "Produit supprimé"}

@app.get("/produits/affichage")
def afficher_tableau(db: Session = Depends(get_db)):
    produits = db.query(ProduitDB).all()
    tableau = [
        {
            "numProduit": p.numProduit,
            "design": p.design,
            "prix": p.prix,
            "quantite": p.quantite,
            "montant": p.prix * p.quantite
        }
        for p in produits
    ]
    return tableau

@app.get("/stats")
def stats(db: Session = Depends(get_db)):
    produits = db.query(ProduitDB).all()
    if not produits:
        return {"min": 0, "max": 0, "total": 0}
    montants = [p.prix * p.quantite for p in produits]
    return {
        "min": min(montants),
        "max": max(montants),
        "total": sum(montants)
    }
