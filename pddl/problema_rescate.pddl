;; =============================================================================
;; PROBLEMA PDDL - RESCATE COMPLETO EN MINA
;; Curso: MIA-103 Fundamentos de Inteligencia Artificial
;; Escenario: 10 víctimas, 3 infraestructuras, 6 unidades móviles
;; =============================================================================

(define (problem rescate-mina-completo)
    (:domain rescate-mina)
    
    ;; =========================================================================
    ;; OBJETOS (Instancias concretas del dominio)
    ;; =========================================================================
    (:objects
        ;; --- LOCACIONES (5) ---
        C0 C1 C2 C3 M - locacion
        
        ;; --- UNIDADES MÓVILES (6) ---
        UM1 UM2 - unidad_movil  ; Capacidad 8 personas c/u
        U1 - unidad_movil       ; Puente PPF + 3 técnicos
        UP - unidad_movil       ; Capacidad 15 personas
        UX - unidad_movil       ; Transporte carga (PCP)
        U3 - unidad_movil       ; Capacidad 10 personas
        
        ;; --- PERSONAL DE RESCATE (4) ---
        Medico1 - medico
        Rescatista1 Rescatista2 - rescatista
        Asistente1 - asistente
        
        ;; --- PERSONAL DE CONSTRUCCIÓN (21) ---
        ; Técnicos para puente C1 (3)
        TecnicoC1_1 TecnicoC1_2 TecnicoC1_3 - tecnico
        
        ; Técnicos para puente colgante C3 (3)
        TecnicoC3_1 TecnicoC3_2 TecnicoC3_3 - tecnico
        
        ; Obreros para carretera C2 (10)
        Obrero1 Obrero2 Obrero3 Obrero4 Obrero5 
        Obrero6 Obrero7 Obrero8 Obrero9 Obrero10 - obrero
        
        ; Ingeniero para carretera
        Ingeniero1 - ingeniero
        
        ; Operador para puente colgante (se queda en C3)
        Operador1 - operador
        
        ;; --- VÍCTIMAS (10) ---
        ; Graves (4) - Requieren estabilización URGENTE
        VG1 VG2 VG3 VG4 - victima_grave
        
        ; Estables (3) - No críticas
        VE1 VE2 VE3 - victima_estable
        
        ; No Afectadas (3) - Sin lesiones
        VNA1 VNA2 VNA3 - victima_no_afectada
        
        ;; --- INFRAESTRUCTURA (3) ---
        PPF - puente            ; Puente prefabricado C1
        Carretera_C2 - carretera ; Carretera 500m C2
        PCP - puente            ; Puente colgante C3
        
        ;; --- MAQUINARIA (4) ---
        Maq1 Maq2 Maq3 Maq4 - maquinaria
    )
    
    ;; =========================================================================
    ;; ESTADO INICIAL (Configuración al inicio del problema)
    ;; =========================================================================
    (:init
        ;; --- CLASIFICACIÓN DE LOCACIONES ---
        (base C0)
        (zona_desastre M)
        (zona_estacionamiento C1)
        (zona_estacionamiento C2)
        (zona_estacionamiento C3)
        
        ;; --- TOPOLOGÍA DE LA RUTA (adyacencia) ---
        (adyacente C0 C1)
        (adyacente C1 C0)  ; Simétrica
        (adyacente C1 C2)
        (adyacente C2 C1)
        (adyacente C2 C3)
        (adyacente C3 C2)
        (adyacente C3 M)
        (adyacente M C3)
        
        ;; --- PERMISOS DE AVANCE INICIAL ---
        (puede_avanzar_a C0)  ; Siempre accesible
        (puede_avanzar_a C1)  ; Siempre accesible desde C0
        ; C2, C3 y M se habilitan al construir infraestructura
        
        ;; --- UNIDADES MÓVILES EN C0 ---
        (en UM1 C0)
        (en UM2 C0)
        (en U1 C0)
        (en UP C0)
        (en UX C0)
        (en U3 C0)
        
        ;; --- CAPACIDADES DE UNIDADES ---
        (espacio_disponible UM1)
        (espacio_disponible UM2)
        (espacio_disponible U1)
        (espacio_disponible UP)
        (espacio_disponible UX)
        (espacio_disponible U3)
        
        ;; Unidades con capacidad de carga
        (puede_transportar_carga U1)
        (puede_transportar_carga UP)
        (puede_transportar_carga UX)
        
        ;; --- PERSONAL DE RESCATE EN C0 ---
        (en Medico1 C0)
        (en Rescatista1 C0)
        (en Rescatista2 C0)
        (en Asistente1 C0)
        
        (disponible Medico1)
        (disponible Rescatista1)
        (disponible Rescatista2)
        (disponible Asistente1)
        
        ;; --- CAPACIDADES DEL PERSONAL DE RESCATE ---
        (puede_estabilizar Medico1)
        (puede_trasladar Rescatista1)
        (puede_trasladar Rescatista2)
        
        ;; --- PERSONAL DE CONSTRUCCIÓN EN C0 ---
        (en TecnicoC1_1 C0)
        (en TecnicoC1_2 C0)
        (en TecnicoC1_3 C0)
        (en TecnicoC3_1 C0)
        (en TecnicoC3_2 C0)
        (en TecnicoC3_3 C0)
        (en Obrero1 C0)
        (en Obrero2 C0)
        (en Obrero3 C0)
        (en Obrero4 C0)
        (en Obrero5 C0)
        (en Obrero6 C0)
        (en Obrero7 C0)
        (en Obrero8 C0)
        (en Obrero9 C0)
        (en Obrero10 C0)
        (en Ingeniero1 C0)
        (en Operador1 C0)
        
        (disponible TecnicoC1_1)
        (disponible TecnicoC1_2)
        (disponible TecnicoC1_3)
        (disponible TecnicoC3_1)
        (disponible TecnicoC3_2)
        (disponible TecnicoC3_3)
        (disponible Obrero1)
        (disponible Obrero2)
        (disponible Obrero3)
        (disponible Obrero4)
        (disponible Obrero5)
        (disponible Obrero6)
        (disponible Obrero7)
        (disponible Obrero8)
        (disponible Obrero9)
        (disponible Obrero10)
        (disponible Ingeniero1)
        (disponible Operador1)
        
        ;; --- INFRAESTRUCTURA EN C0 (Sin construir) ---
        (en PPF C0)
        (en Carretera_C2 C0)
        (en PCP C0)
        
        (not (construido PPF))
        (not (construido Carretera_C2))
        (not (construido PCP))
        
        (not (operativo PPF))
        (not (operativo Carretera_C2))
        (not (operativo PCP))
        
        ;; --- MAQUINARIA EN C0 ---
        (en Maq1 C0)
        (en Maq2 C0)
        (en Maq3 C0)
        (en Maq4 C0)
        
        ;; --- VÍCTIMAS EN LA MINA (M) ---
        ; Víctimas graves
        (en VG1 M)
        (en VG2 M)
        (en VG3 M)
        (en VG4 M)
        
        (disponible VG1)
        (disponible VG2)
        (disponible VG3)
        (disponible VG4)
        
        (requiere_estabilizacion VG1)
        (requiere_estabilizacion VG2)
        (requiere_estabilizacion VG3)
        (requiere_estabilizacion VG4)
        
        (not (estabilizado VG1))
        (not (estabilizado VG2))
        (not (estabilizado VG3))
        (not (estabilizado VG4))
        
        ; Víctimas estables
        (en VE1 M)
        (en VE2 M)
        (en VE3 M)
        
        (disponible VE1)
        (disponible VE2)
        (disponible VE3)
        
        ; Víctimas no afectadas
        (en VNA1 M)
        (en VNA2 M)
        (en VNA3 M)
        
        (disponible VNA1)
        (disponible VNA2)
        (disponible VNA3)
    )
    
    ;; =========================================================================
    ;; META (Condiciones que deben cumplirse)
    ;; =========================================================================
    (:goal (and
        ;; --- TODAS LAS VÍCTIMAS RESCATADAS ---
        ; Víctimas graves
        (rescatado VG1)
        (rescatado VG2)
        (rescatado VG3)
        (rescatado VG4)
        
        ; Víctimas estables
        (rescatado VE1)
        (rescatado VE2)
        (rescatado VE3)
        
        ; Víctimas no afectadas
        (rescatado VNA1)
        (rescatado VNA2)
        (rescatado VNA3)
        
        ;; --- TODAS LAS VÍCTIMAS GRAVES ESTABILIZADAS ---
        (estabilizado VG1)
        (estabilizado VG2)
        (estabilizado VG3)
        (estabilizado VG4)
        
        ;; --- TODAS LAS VÍCTIMAS EN LA BASE ---
        (en VG1 C0)
        (en VG2 C0)
        (en VG3 C0)
        (en VG4 C0)
        (en VE1 C0)
        (en VE2 C0)
        (en VE3 C0)
        (en VNA1 C0)
        (en VNA2 C0)
        (en VNA3 C0)
        
        ;; --- INFRAESTRUCTURA CONSTRUIDA ---
        (construido PPF)
        (construido Carretera_C2)
        (construido PCP)
        
        ;; --- OPERATIVO ---
        (operativo PPF)
        (operativo Carretera_C2)
        (operativo PCP)
    ))
)

