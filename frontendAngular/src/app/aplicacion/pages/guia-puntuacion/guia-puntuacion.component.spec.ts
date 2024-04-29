import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GuiaPuntuacionComponent } from './guia-puntuacion.component';

describe('GuiaPuntuacionComponent', () => {
  let component: GuiaPuntuacionComponent;
  let fixture: ComponentFixture<GuiaPuntuacionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [GuiaPuntuacionComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(GuiaPuntuacionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
