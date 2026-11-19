"""Run bounded regression; preserve known baseline failures as failures."""
from pathlib import Path
import argparse, importlib.util, io, json, os, re, sys, unittest

args=argparse.ArgumentParser()
args.add_argument('--git-helper',required=True,type=Path)
options=args.parse_args()
ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT/'packages/kernel'), str(ROOT/'packages/workflow')]
assert options.git_helper.is_file(), 'Existing Git test helper is required'
os.environ['L1_GITHUB_TEST_HELPER'] = str(options.git_helper.resolve())
SETS = {
    'kernel': ['test_recovery_reports_v0746','test_kernel','test_plus_registry_v0714','test_github_docs_layout_v077',
               'test_work_docs_navigation_v0724','test_step12_profiles','test_step13_profiles_transfer',
               'test_feature_stage4_export','test_multi_work_ux_v070'],
    'workflow': ['test_recovery_intake_v1675','test_feature_stage4_evidence','test_github_docs_layout_v161','test_personal_github_docs_v150'],
}
expected = {'test_auto_sync_false_skips_implicit_but_not_explicit',
            'test_docs_push_local_git_commit_push_and_remote_sha_readback',
            'test_docs_push_migrates_tracked_legacy_layout_in_one_commit'}
baseline_log = (ROOT/'baseline_workflow_test_log.txt').read_text()
baseline_failures = set(re.findall(r'^(?:FAIL|ERROR): (test_\w+)', baseline_log, re.M))
assert baseline_failures == expected, 'Baseline failure evidence differs'
summary = {}
for package, names in SETS.items():
    suite = unittest.TestSuite(); files = []
    for name in names:
        path = ROOT/'packages'/package/'tests'/(name+'.py')
        spec = importlib.util.spec_from_file_location(package+'_'+name, path)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        group = unittest.defaultTestLoader.loadTestsFromModule(module)
        files.append({'file':name+'.py','tests':group.countTestCases()}); suite.addTests(group)
    stream = io.StringIO(); result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    (ROOT/(package+'_test_log.txt')).write_text(stream.getvalue())
    failures = {case._testMethodName for case, _ in result.failures+result.errors}
    allowed = expected if package == 'workflow' else set()
    summary[package] = {'tests':result.testsRun,'passed':result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),
                        'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),
                        'failing_tests':sorted(failures),'new_regressions':sorted(failures-allowed),'files':files}
    assert failures == allowed, package+': unexpected failure/baseline drift'
summary['status'] = 'NEW_TESTS_PASS_BASELINE_FAILURES_UNCHANGED'
summary['baseline_failing_tests'] = sorted(baseline_failures)
(ROOT/'TEST_RESULTS.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
