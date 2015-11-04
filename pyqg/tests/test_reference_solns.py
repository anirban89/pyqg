import unittest
import numpy as np
import pyqg

class ReferenceSolutionsTester(unittest.TestCase):

    def test_two_layer(self):
        """ Tests against some statistics of a reference two-layer solution """

        year = 360*86400.
        m = pyqg.QGModel(
            nx=32,                      
            L=1e6,                      
            beta=1.5e-11,               
            rek=5.787e-7,               
            rd=30000.0,                 
            delta=0.25,                 
            U1=0.05,                    
            U2=0.0,                     
            filterfac=18.4,
            dt=12800.,                   
            tmax=3*year,          
            tavestart=1*year*0,     
            taveint=12800.,
            useAB2=True,
            diagnostics_list='all'     
            )

        m.set_q1q2(
                (1e-6*np.cos(2*5*np.pi * m.x / m.L) +
                 1e-7*np.cos(2*5*np.pi * m.y / m.W)),
                np.zeros_like(m.x) )
                    
        m.run()

        q1 = m.q[0] 
        q1norm = (q1**2).sum()

        assert m.t == 93312000.0
   
        
        # machine + numpy.version fluctuations
        #   appears to be less than 1%
        rtol, atol = 0.01, 0.

        np.testing.assert_allclose(q1norm, 9.561430503712755e-08, rtol=rtol, atol=atol,
                    err_msg= ' Inconsistent with reference solution')

        diagnostic_results = {
                'APEgen': 2.5225558013107688e-07  / (m.nx**2),
                'EKEdiss': 1.4806764171539711e-07 / (m.nx**2),           
                }

        # just skip all the other tests for now
        #return
        
        ## raw diagnostics (scalar output)
        #diagnostic_results = {
        #    'EKE1': 5.695448642915733e-03,
        #    'EKE2': 1.088253274803528e-04,
        #    'APEgen': 8.842056320175081e-08,
        #    'EKEdiss': 6.368668363708053e-08,        
        #}

        ## old values
        #diagnostic_results = {
        #    'EKE1': 0.008183776317328265,
        #    'EKE2': 0.00015616609033468579,
        #    'APEgen': 2.5225558013107688e-07,
        #    'EKEdiss': 1.4806764171539711e-07,        
        #}
        
        ## need to average these diagnostics
        #avg_diagnostic_results = {
        #    'entspec': 5.703438193477885e-07,
        #    'APEflux': 9.192940039964286e-05,
        #    'KEflux': 1.702621259427053e-04,
        #    'APEgenspec': 9.058591846403974e-05,
        #    'KE1spec': 3.338261440237941e+03,
        #    'KE2spec': 7.043282793801889e+01
        #}
        
        ## old values
        #avg_diagnostic_results = {
        #    'entspec': 1.5015983257921716e-06,,
        #    'APEflux': 0.00017889483037254459,
        #    'KEflux':  0.00037067750708912918,
        #    'APEgenspec': 0.00025837684260178754,
        #    'KE1spec': 8581.3114357188006,,
        #    'KE2spec': 163.75201433878425
        #}    
        
        # first print all output
        for name, des in diagnostic_results.iteritems():
            res = m.get_diagnostic(name)
            print '%10s: %1.15e \n%10s  %1.15e (desired)' % (name, res, '', des)
        #for name, des in avg_diagnostic_results.iteritems():
        #    res = np.abs(m.get_diagnostic(name)).sum()
        #    print '%10s: %1.15e \n%10s  %1.15e (desired)' % (name, res, '', des)

        # now do assertions
        for name, des in diagnostic_results.iteritems():
            res = m.get_diagnostic(name)
            np.testing.assert_allclose(res, des, rtol=rtol, atol=atol)
        #for name, des in avg_diagnostic_results.iteritems():
        #    res = np.abs(m.get_diagnostic(name)).sum()
        #    np.testing.assert_allclose(res, des, rtol=rtol, atol=atol)

        # just skip all the other tests for now
        return
        
        ## raw diagnostics (scalar output)
        diagnostic_results = {
            'EKE1': 5.695448642915733e-03,
            'EKE2': 1.088253274803528e-04,
            'APEgen': 8.842056320175081e-08,
            'EKEdiss': 6.368668363708053e-08,        
        }
        ## old values
        #diagnostic_results = {
        #    'EKE1': 0.008183776317328265,
        #    'EKE2': 0.00015616609033468579,
        #    'APEgen': 2.5225558013107688e-07,
        #    'EKEdiss': 1.4806764171539711e-07,        
        #}
        
        ## need to average these diagnostics
        avg_diagnostic_results = {
            'entspec': 5.703438193477885e-07,
            'APEflux': 9.192940039964286e-05,
            'KEflux': 1.702621259427053e-04,
            'APEgenspec': 9.058591846403974e-05,
            'KE1spec': 3.338261440237941e+03,
            'KE2spec': 7.043282793801889e+01
        }
        
        ## old values
        #avg_diagnostic_results = {
        #    'entspec': 1.5015983257921716e-06,,
        #    'APEflux': 0.00017889483037254459,
        #    'KEflux':  0.00037067750708912918,
        #    'APEgenspec': 0.00025837684260178754,
        #    'KE1spec': 8581.3114357188006,,
        #    'KE2spec': 163.75201433878425
        #}    
        
        # first print all output
        for name, des in diagnostic_results.iteritems():
            res = m.get_diagnostic(name)
            print '%10s: %1.15e \n%10s  %1.15e (desired)' % (name, res, '', des)
        for name, des in avg_diagnostic_results.iteritems():
            res = np.abs(m.get_diagnostic(name)).sum()
            print '%10s: %1.15e \n%10s  %1.15e (desired)' % (name, res, '', des)

        # now do assertions
        for name, des in diagnostic_results.iteritems():
            res = m.get_diagnostic(name)
            np.testing.assert_allclose(res, des, rtol)
        for name, des in avg_diagnostic_results.iteritems():
            res = np.abs(m.get_diagnostic(name)).sum()
            np.testing.assert_allclose(res, des, rtol)

    def test_bt(self):
        """ Tests against some statistics of a reference barotropic solution """

        m = pyqg.BTModel(L=2.*np.pi,nx=64, tmax = 5,
                beta = 0., H = 1., rek = 0., rd = None, dt = 0.0025,
                twrite=1000)

        # IC
        p = np.exp(-(2.*(m.x-1.75*np.pi/2))**2.-(2.*(m.y-np.pi))**2) +\
                np.exp(-(2.*(m.x-2.25*np.pi/2))**2.-(2.*(m.y-np.pi))**2)

        ph = m.fft(p[np.newaxis,...])
        KEaux = m.spec_var(m.filtr*m.wv*ph )/2.
        pih = ( ph/np.sqrt(KEaux) )
        qih = -m.wv2*pih
        qi = m.ifft(qih)
        m.set_q(qi)
       
        rtol = 1.e-5
        atol = 1.e-14

        np.testing.assert_allclose(m.q, qi, rtol, atol)

        m.run()

        qnorm = (m.q**2).sum()
        mp = m.ifft(m.ph)
        pnorm = (mp**2).sum()
        ke = m._calc_ke()

        print 'time:       %g' % m.t
        assert m.t == 5.000000000000082
        
        np.testing.assert_allclose(qnorm, 89101.741238768518, rtol, atol,
                err_msg= ' Inconsistent with reference solution')
        np.testing.assert_allclose(pnorm, 1493.217664248918, rtol, atol,
                err_msg= ' Inconsistent with reference solution')
        np.testing.assert_allclose(ke, 0.9950360837282386, rtol, atol,
                err_msg= ' Inconsistent with reference solution')

    def test_sqg(self):
        """ Tests against some statistics of a reference sqg solution """

        m = pyqg.SQGModel(L=2.*np.pi,nx=64, tmax = 5.,
                beta = 0., H = 1., rek = 0., dt = 0.0025,
                twrite=1000)

        p = np.exp(-(2.*(m.x-1.75*np.pi/2))**2.-(2.*(m.y-np.pi))**2) +\
                np.exp(-(2.*(m.x-2.25*np.pi/2))**2.-(2.*(m.y-np.pi))**2)

        ph = m.fft(p[np.newaxis,:,:])
        KEaux = m.spec_var( m.filtr*m.wv*ph )/2.
        ph = ( ph/np.sqrt(KEaux) )
        qih = m.wv*ph
        qi = m.ifft(qih)
        m.set_q(qi)

        rtol = 1.e-5
        atol = 1.e-14

        np.testing.assert_allclose(m.q, qi, atol)

        m.run()

        qnorm = (m.q**2).sum()
        mp = m.ifft(m.ph)
        pnorm = (mp**2).sum()
        ke = m._calc_ke()

        print 'time:       %g' % m.t
        assert m.t == 5.000000000000082
        
        np.testing.assert_allclose(qnorm, 7847.5169609881032, rtol, atol,
                err_msg= ' Inconsistent with reference solution')
        np.testing.assert_allclose(pnorm, 1346.8874163575524, rtol, atol,
                err_msg= ' Inconsistent with reference solution')
        np.testing.assert_allclose(ke, 0.9579493831013508, rtol, atol,
                err_msg= ' Inconsistent with reference solution')


if __name__ == "__main__":
    unittest.main()
