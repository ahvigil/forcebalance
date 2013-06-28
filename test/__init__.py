import unittest
import os, sys, time
import traceback
from collections import OrderedDict

class ForceBalanceTestCase(unittest.TestCase):
    def __init__(self,methodName='runTest'):
        super(ForceBalanceTestCase,self).__init__(methodName)
        self.longMessage=True

    def shortDescription(self):
        """Default shortDescription function returns None value if no description
        is present, but this causes errors when trying to print. Return empty
        string instead"""

        message = super(ForceBalanceTestCase,self).shortDescription()
        if message: return message
        else: return self.id()

class ForceBalanceTestResult(unittest.TestResult):
    """This manages the reporting of test results as they are run,
       and also records results in the internal data structures provided
       by unittest.TestResult"""

    def startTest(self, test):
        super(ForceBalanceTestResult, self).startTest(test)
        sys.stderr.write("---     " + test.shortDescription())
        print "<<<<<<<< Starting %s >>>>>>>>\n" % test.id()

    def addFailure(self, test, err):
        super(ForceBalanceTestResult, self).addFailure(test,err)
        sys.stderr.write("\r\x1b[31;1m" + "FAIL" + "\x1b[0m    " + test.shortDescription() + "\n")
        
        errorMessage = self.buildErrorMessage(test, err)

        for line in errorMessage.splitlines():
            sys.stderr.write("\t >\t" + line + "\n")

    def addError(self, test, err):
        super(ForceBalanceTestResult, self).addError(test,err)
        sys.stderr.write("\r\x1b[33;1mERROR\x1b[0m   " + test.shortDescription() + "\n")

        errorMessage = self.buildErrorMessage(test,err)

        for line in errorMessage.splitlines():
            sys.stderr.write("\t >\t" + line + "\n")
    
    def buildErrorMessage(self, test, err):
        """Compile error data from test exceptions into a helpful message"""
        errorMessage = ""
        errorMessage += test.id()
        errorMessage += "\n\n"

        errorMessage += traceback.format_exc() + "\n"
        return errorMessage

    def addSuccess(self, test):
        sys.stderr.write("\r\x1b[32mOK\x1b[0m      " + test.shortDescription() + "\n")

    def addSkip(self, test, err=""):
        sys.stderr.write("\r\x1b[33;1mSKIP\x1b[0m    " + test.shortDescription() + "\n")
        if err: sys.stderr.write("\t\t%s\n" % err)

    def stopTest(self, test):
        print "\n<<<<<<<< Finished %s >>>>>>>>\n\n" % test.id()

    def startTestRun(self, test):
        self.runTime= time.time()

    def stopTestRun(self, test):
        self.runTime = time.time()-self.runTime
        sys.stderr.write("\n<run=%d errors=%d fail=%d in %.2fs>\n" % (self.testsRun,len(self.errors),len(self.failures), self.runTime))
        if self.wasSuccessful(): sys.stderr.write("All tests passed successfully")
        else: sys.stderr.write("Some tests failed or had errors!")

class ForceBalanceTestRunner(object):
    """This test runner class manages the running and logging of tests.
       It controls WHERE test results go but not what is recorded.
       Once the tests have finished running, it will return the test result
       for further analysis"""

    def run(self,test_modules=[],exclude=[],pretend=False,program_output='test/test.log',quick=False):   
        unittest.installHandler()

        tests = unittest.TestSuite()
        for module in test_modules:
            try:
                m=__import__(module)
                module_tests=unittest.defaultTestLoader.loadTestsFromModule(m)
                tests.addTests(module_tests)
            except: print "Error loading '%s'" % module

        result = ForceBalanceTestResult()

        ### TEST IS RUNNING ###
        result.startTestRun(tests)
        if pretend:
            for module in tests:
                for test in module:
                    try:
                        result.addSkip(test)
                    except AttributeError: continue
        else:
            self.console = sys.stdout
            sys.stdout = open(program_output, 'w')

            unittest.registerResult(result)
            tests.run(result)
            

            sys.stdout.close()
            sys.stdout = self.console

        result.stopTestRun(tests)
        ### TEST IS STOPPED ###

        return result
        
class TestValues(object):
    cwd = os.getcwd()
    water_options={
            'penalty_type': 'L2',
            'print_gradient': 1, 
            'eig_lowerbound': 0.0001, 
            'error_tolerance': 0.0, 
            'scanindex_name': [], 
            'read_mvals': None, 
            'maxstep': 100, 
            'print_parameters': 1, 
            'penalty_hyperbolic_b': 1e-06, 
            'gmxsuffix': '', 
            'readchk': None, 
            'mintrust': 0.0, 
            'penalty_multiplicative': 0.0, 
            'convergence_step': 0.0001, 
            'adaptive_damping': 0.5, 
            'finite_difference_h': 0.001, 
            'wq_port': 0, 
            'verbose_options': 0,
            'scan_vals': None,
            'logarithmic_map': 0,
            'writechk_step': 1,
            'forcefield': ['water.itp'],
            'use_pvals': 0,
            'scanindex_num': [],
            'normalize_weights': 1,
            'adaptive_factor': 0.25,
            'trust0': 0.1,
            'penalty_additive': 0.01,
            'gmxpath': '/usr/bin',
            'writechk': None,
            'print_hessian': 0,
            'have_vsite': 0,
            'tinkerpath': '',
            'ffdir': 'forcefield',
            'constrain_charge': 0,
            'convergence_gradient': 0.0001,
            'convergence_objective': 0.0001,
            'backup': 1,
            'rigid_water': 0,
            'search_tolerance': 0.0001,
            'objective_history': 2,
            'amoeba_polarization': 'direct',
            'lm_guess': 1.0,
            'priors': OrderedDict(),
            'asynchronous': 0,
            'read_pvals': None,
            'root': cwd + '/studies/001_water_tutorial',
            'jobtype': 'NEWTON',
            'penalty_alpha': 0.001}
    tgt_opts = [
        {   'fdgrad': 0, 
            'qmboltz': 0.0, 
            'gas_prod_steps': 0, 
            'force': 1, 
            'weight': 1.0, 
            'fd_ptypes': [], 
            'resp': 0, 
            'sleepy': 0, 
            'fitatoms': 0, 
            'w_force': 1.0, 
            'w_cp': 1.0, 
            'batch_fd': 0, 
            'w_resp': 0.0, 
            'force_cuda': 0, 
            'w_netforce': 0.0, 
            'mts_vvvr': 0, 
            'do_cosmo': 0, 
            'quadrupole_denom': 1.0, 
            'self_pol_mu0': 0.0, 
            'qmboltztemp': 298.15, 
            'force_map': 'residue', 
            'self_pol_alpha': 0.0, 
            'wavenumber_tol': 10.0, 
            'energy_upper': 30.0, 
            'cauchy': 0, 
            'w_torque': 0.0, 
            'w_alpha': 1.0, 
            'w_eps0': 1.0, 
            'openmm_cuda_precision': '', 
            'gas_equ_steps': 0, 
            'masterfile': 'interactions.txt', 
            'absolute': 0, 
            'type': 'ABINITIO_GMX', 
            'anisotropic_box': 0, 
            'fragment1': '', 
            'rmsd_denom': 0.1, 
            'dipole_denom': 1.0, 
            'fdhessdiag': 0, 
            'energy': 1, 
            'energy_denom': 1.0, 
            'covariance': 0, 
            'hvap_subaverage': 0, 
            'optimize_geometry': 1, 
            'liquid_interval': 0.05, 
            'w_energy': 1.0, 
            'w_rho': 1.0, 
            'liquid_equ_steps': 10000, 
            'fragment2': '', 
            'name': 'cluster-06', 
            'w_hvap': 1.0, 
            'w_kappa': 1.0, 
            'attenuate': 0, 
            'polarizability_denom': 1.0, 
            'manual': 0, 
            'run_internal': 1, 
            'sampcorr': 0, 
            'fdhess': 0, 
            'liquid_prod_steps': 20000, 
            'liquid_timestep': 0.5, 
            'shots': -1, 
            'resp_a': 0.001, 
            'resp_b': 0.1, 
            'whamboltz': 0, 
            'all_at_once': 1},
        {   'fdgrad': 0, 
            'qmboltz': 0.0, 
            'gas_prod_steps': 0, 
            'force': 1, 
            'weight': 1.0, 
            'fd_ptypes': [], 
            'resp': 0, 
            'sleepy': 0, 
            'fitatoms': 0, 
            'w_force': 1.0, 
            'w_cp': 1.0, 
            'batch_fd': 0, 
            'w_resp': 0.0, 
            'force_cuda': 0, 
            'w_netforce': 0.0, 
            'mts_vvvr': 0, 
            'do_cosmo': 0, 
            'quadrupole_denom': 1.0, 
            'self_pol_mu0': 0.0, 
            'qmboltztemp': 298.15, 
            'force_map': 'residue', 
            'self_pol_alpha': 0.0, 
            'wavenumber_tol': 10.0, 
            'energy_upper': 30.0, 
            'cauchy': 0, 
            'w_torque': 0.0, 
            'w_alpha': 1.0, 
            'w_eps0': 1.0, 
            'openmm_cuda_precision': '', 
            'gas_equ_steps': 0, 
            'masterfile': 'interactions.txt', 
            'absolute': 0, 
            'type': 'ABINITIO_GMX', 
            'anisotropic_box': 0, 
            'fragment1': '', 
            'rmsd_denom': 0.1, 
            'dipole_denom': 1.0, 
            'fdhessdiag': 0, 
            'energy': 1, 
            'energy_denom': 1.0, 
            'covariance': 0, 
            'hvap_subaverage': 0, 
            'optimize_geometry': 1, 
            'liquid_interval': 0.05, 
            'w_energy': 1.0, 
            'w_rho': 1.0, 
            'liquid_equ_steps': 10000, 
            'fragment2': '', 
            'name': 'cluster-12', 
            'w_hvap': 1.0, 
            'w_kappa': 1.0, 
            'attenuate': 0, 
            'polarizability_denom': 1.0, 
            'manual': 0, 
            'run_internal': 1, 
            'sampcorr': 0, 
            'fdhess': 0, 
            'liquid_prod_steps': 20000, 
            'liquid_timestep': 0.5, 
            'shots': -1, 
            'resp_a': 0.001, 
            'resp_b': 0.1, 
            'whamboltz': 0, 
            'all_at_once': 1}
    ]