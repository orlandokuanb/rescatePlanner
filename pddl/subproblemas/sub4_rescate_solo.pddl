;; =============================================================================
;; SUB-PROBLEMA 4: RESCATE DE VÍCTIMAS
;; Precondición: TODA la infraestructura construida y operativa
;; Objetivo: Rescatar las 10 víctimas, estabilizar graves
;; =============================================================================

(define (problem sub4-rescate-solo)
    (:domain rescate-mina)
    
    (:objects
        C0 C1 C2 C3 M - locacion
        UM1 UM2 - unidad_movil
        
        Medico1 - medico
        Rescatista1 Rescatista2 - rescatista
        Asistente1 - asistente
        
        VG1 VG2 VG3 VG4 - victima_grave
        VE1 VE2 VE3 - victima_estable
        VNA1 VNA2 VNA3 - victima_no_afectada
        
        PPF PCP - puente
        Carretera_C2 - carretera
    )
    
    (:init
        ;; Clasificación
        (base C0)
        (zona_desastre M)
        
        ;; Topología
        (adyacente C0 C1)
        (adyacente C1 C0)
        (adyacente C1 C2)
        (adyacente C2 C1)
        (adyacente C2 C3)
        (adyacente C3 C2)
        (adyacente C3 M)
        (adyacente M C3)
        
        ;; TODA la infraestructura operativa (precondición)
        (puede_avanzar_a C0)
        (puede_avanzar_a C1)
        (puede_avanzar_a C2)
        (puede_avanzar_a C3)
        (puede_avanzar_a M)
        
        (construido PPF)
        (operativo PPF)
        (conecta PPF C1 C2)
        
        (construido Carretera_C2)
        (operativo Carretera_C2)
        (conecta Carretera_C2 C2 C3)
        
        (construido PCP)
        (operativo PCP)
        (conecta PCP C3 M)
        
        ;; Unidades en C0
        (en UM1 C0)
        (en UM2 C0)
        (espacio_disponible UM1)
        (espacio_disponible UM2)
        
        ;; Personal de rescate en C0
        (en Medico1 C0)
        (en Rescatista1 C0)
        (en Rescatista2 C0)
        (en Asistente1 C0)
        
        (disponible Medico1)
        (disponible Rescatista1)
        (disponible Rescatista2)
        (disponible Asistente1)
        
        (puede_estabilizar Medico1)
        (puede_trasladar Rescatista1)
        (puede_trasladar Rescatista2)
        
        ;; Víctimas en la mina
        (en VG1 M) (disponible VG1) (requiere_estabilizacion VG1) (not (estabilizado VG1))
        (en VG2 M) (disponible VG2) (requiere_estabilizacion VG2) (not (estabilizado VG2))
        (en VG3 M) (disponible VG3) (requiere_estabilizacion VG3) (not (estabilizado VG3))
        (en VG4 M) (disponible VG4) (requiere_estabilizacion VG4) (not (estabilizado VG4))
        
        (en VE1 M) (disponible VE1)
        (en VE2 M) (disponible VE2)
        (en VE3 M) (disponible VE3)
        
        (en VNA1 M) (disponible VNA1)
        (en VNA2 M) (disponible VNA2)
        (en VNA3 M) (disponible VNA3)
    )
    
    (:goal (and
        ;; Todas las víctimas rescatadas
        (rescatado VG1) (rescatado VG2) (rescatado VG3) (rescatado VG4)
        (rescatado VE1) (rescatado VE2) (rescatado VE3)
        (rescatado VNA1) (rescatado VNA2) (rescatado VNA3)
        
        ;; Víctimas graves estabilizadas
        (estabilizado VG1)
        (estabilizado VG2)
        (estabilizado VG3)
        (estabilizado VG4)
        
        ;; Todas en la base
        (en VG1 C0) (en VG2 C0) (en VG3 C0) (en VG4 C0)
        (en VE1 C0) (en VE2 C0) (en VE3 C0)
        (en VNA1 C0) (en VNA2 C0) (en VNA3 C0)
    ))
)

