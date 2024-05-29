import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GestionColaboradoresComponent } from './gestion-colaboradores.component';

describe('GestionColaboradoresComponent', () => {
  let component: GestionColaboradoresComponent;
  let fixture: ComponentFixture<GestionColaboradoresComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [GestionColaboradoresComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(GestionColaboradoresComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
