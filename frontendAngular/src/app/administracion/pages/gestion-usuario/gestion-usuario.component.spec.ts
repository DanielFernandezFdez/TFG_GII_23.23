import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GestionUsuarioComponent } from './gestion-usuario.component';

describe('GestionUsuarioComponent', () => {
  let component: GestionUsuarioComponent;
  let fixture: ComponentFixture<GestionUsuarioComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [GestionUsuarioComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(GestionUsuarioComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
